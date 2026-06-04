import nltk
from collections import Counter

from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download("vader_lexicon", quiet=True)


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "categoria_original": "tecnologia"
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
        "categoria_original": "tecnologia"
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación.",
        "categoria_original": "economia"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio preocupante sobre el calentamiento global.",
        "categoria_original": "ciencia"
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "categoria_original": "gobierno"
    }
]


class ClasificadorNoticias:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.clasificador = LinearSVC(max_iter=2000)
        self.categorias = []
        self.entrenado = False

    def entrenar(self, textos, etiquetas):
        X = self.vectorizer.fit_transform(textos)
        self.clasificador.fit(X, etiquetas)

        self.categorias = sorted(list(set(etiquetas)))
        self.entrenado = True

        scores = cross_val_score(
            self.clasificador,
            X,
            etiquetas,
            cv=min(3, len(textos) // 2)
        )

        return {
            "accuracy_cv": scores.mean(),
            "categorias": self.categorias,
            "n_muestras": len(textos),
        }

    def predecir(self, textos):
        X = self.vectorizer.transform(textos)
        return self.clasificador.predict(X)

    def predecir_con_confianza(self, texto):
        X = self.vectorizer.transform([texto])
        decision = self.clasificador.decision_function(X)[0]
        prediccion = self.clasificador.predict(X)[0]

        return prediccion, dict(zip(self.clasificador.classes_, decision))


class AnalizadorSentimientos:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analizar(self, texto):
        scores = self.sia.polarity_scores(texto)
        compound = scores["compound"]

        if compound >= 0.05:
            etiqueta = "positivo"
        elif compound <= -0.05:
            etiqueta = "negativo"
        else:
            etiqueta = "neutral"

        return {
            "positivo": scores["pos"],
            "negativo": scores["neg"],
            "neutral": scores["neu"],
            "compound": compound,
            "etiqueta": etiqueta,
        }

    def analizar_corpus(self, documentos):
        resultados = [self.analizar(doc) for doc in documentos]
        distribucion = Counter(r["etiqueta"] for r in resultados)
        promedio = sum(r["compound"] for r in resultados) / len(resultados)

        return resultados, {
            "distribucion": dict(distribucion),
            "sentimiento_promedio": promedio,
            "tono_general": (
                "positivo" if promedio > 0.05
                else "negativo" if promedio < -0.05
                else "neutral"
            ),
        }


textos_entrenamiento = [
    "inteligencia artificial machine learning algoritmos redes neuronales deep learning",
    "nuevo procesador computadora software desarrollo programación tecnología",
    "startup tecnológica lanza aplicación innovadora plataforma digital",
    "robot automatización industria software empresa tecnología",

    "mercados financieros bolsa acciones inversión capital rendimiento",
    "inflación economía banco central tasas interés política monetaria",
    "desempleo crisis económica recesión PIB crecimiento producto interno",
    "comercio internacional exportaciones importaciones aranceles tratado",

    "estudio científico investigadores descubrimiento laboratorio publicación",
    "cambio climático calentamiento global temperatura emisiones carbono",
    "vacuna tratamiento médico salud enfermedad hospital pacientes",
    "espacio NASA cohete satélite misión exploración astronauta",

    "elecciones candidato presidente congreso voto democracia partido",
    "gobierno ley reforma política pública decreto legislación",
    "seguridad pública policía crimen delito justicia tribunal",
    "presupuesto gasto público programa social gobierno federal",
]

etiquetas_entrenamiento = [
    "tecnologia", "tecnologia", "tecnologia", "tecnologia",
    "economia", "economia", "economia", "economia",
    "ciencia", "ciencia", "ciencia", "ciencia",
    "politica", "politica", "politica", "politica",
]


clasificador = ClasificadorNoticias()
resultado_entrenamiento = clasificador.entrenar(
    textos_entrenamiento,
    etiquetas_entrenamiento
)

print("=== FASE 3.1: Clasificador de Noticias ===\n")

print("Entrenamiento completado:")
print(f"  Muestras: {resultado_entrenamiento['n_muestras']}")
print(f"  Categorías: {resultado_entrenamiento['categorias']}")
print(f"  Accuracy CV: {resultado_entrenamiento['accuracy_cv']:.3f}")

print("\nClasificación automática de noticias del SIMANW:")

for noticia in noticias:
    texto = f"{noticia['titulo']} {noticia['cuerpo']}"
    prediccion, scores = clasificador.predecir_con_confianza(texto)

    noticia["categoria_predicha"] = prediccion

    print(f"\nTítulo: {noticia['titulo']}")
    print(f"Cat. original: {noticia['categoria_original']}")
    print(f"Cat. predicha: {prediccion}")

    top_scores = sorted(scores.items(), key=lambda x: -x[1])[:3]
    print("Scores:", ", ".join(f"{c}={s:.2f}" for c, s in top_scores))


analizador_sent = AnalizadorSentimientos()

print("\n=== FASE 3.2: Análisis de Sentimientos ===\n")

textos_noticias = [n["cuerpo"] for n in noticias]
resultados_sent, resumen_sent = analizador_sent.analizar_corpus(textos_noticias)

for noticia, sent in zip(noticias, resultados_sent):
    noticia["sentimiento"] = sent

    indicador = (
        "↑" if sent["etiqueta"] == "positivo"
        else "↓" if sent["etiqueta"] == "negativo"
        else "→"
    )

    print(f"{indicador} [{sent['compound']:+.3f}] {noticia['titulo']}")
    print(f"  Sentimiento: {sent['etiqueta']}")

print("\n--- Resumen de Sentimiento del Corpus ---")
print(f"Distribución: {resumen_sent['distribucion']}")
print(f"Promedio: {resumen_sent['sentimiento_promedio']:+.3f}")
print(f"Tono general: {resumen_sent['tono_general'].upper()}")