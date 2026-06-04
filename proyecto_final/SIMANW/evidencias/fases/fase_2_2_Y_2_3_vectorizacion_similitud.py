import re
import nltk
from collections import Counter

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


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
        "cuerpo": "Un equipo internacional publicó un estudio sobre el calentamiento global.",
        "categoria_original": "ciencia"
    }
]


class PipelineNLP:
    def __init__(self, idioma="spanish"):
        self.idioma = idioma
        self.stemmer = SnowballStemmer(idioma)
        self.stop_words = set(stopwords.words(idioma))

    def limpiar(self, texto):
        texto = texto.lower()
        texto = re.sub(r"[^\w\sáéíóúñü]", " ", texto)
        texto = re.sub(r"\d+", "", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto

    def tokenizar(self, texto):
        return word_tokenize(texto, language=self.idioma)

    def eliminar_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stop_words and len(t) > 2]

    def aplicar_stemming(self, tokens):
        return [self.stemmer.stem(t) for t in tokens]

    def procesar(self, texto):
        limpio = self.limpiar(texto)
        tokens = self.tokenizar(limpio)
        sin_sw = self.eliminar_stopwords(tokens)
        stems = self.aplicar_stemming(sin_sw)

        return {
            "original": texto,
            "limpio": limpio,
            "tokens": tokens,
            "sin_stopwords": sin_sw,
            "stems": stems,
            "num_oraciones": len(sent_tokenize(texto, language=self.idioma)),
            "vocabulario_unico": len(set(sin_sw)),
            "riqueza_lexica": len(set(sin_sw)) / max(len(sin_sw), 1),
        }


class RepresentacionVectorial:
    def __init__(self, max_features=2000, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True
        )
        self.matriz = None
        self.documentos_texto = []

    def construir_matriz(self, documentos):
        self.documentos_texto = documentos
        self.matriz = self.vectorizer.fit_transform(documentos)
        return self.matriz

    def vocabulario(self):
        return self.vectorizer.get_feature_names_out()

    def top_terminos_documento(self, doc_idx, n=8):
        vector = self.matriz[doc_idx].toarray().flatten()
        terminos = self.vocabulario()
        indices_top = vector.argsort()[::-1][:n]
        return [(terminos[i], vector[i]) for i in indices_top if vector[i] > 0]

    def info_matriz(self):
        return {
            "documentos": self.matriz.shape[0],
            "features": self.matriz.shape[1],
            "densidad": self.matriz.nnz / (self.matriz.shape[0] * self.matriz.shape[1]),
            "terminos_promedio_doc": self.matriz.nnz / self.matriz.shape[0],
        }


class CalculadorSimilitud:
    def __init__(self, matriz_tfidf):
        self.matriz = matriz_tfidf
        self.sim_matrix = cosine_similarity(matriz_tfidf)

    def similitud_par(self, doc_i, doc_j):
        return self.sim_matrix[doc_i][doc_j]

    def documentos_similares(self, doc_idx, top_n=3):
        similitudes = self.sim_matrix[doc_idx]
        indices = similitudes.argsort()[::-1][1:top_n + 1]
        return [(idx, similitudes[idx]) for idx in indices]

    def agrupar_por_similitud(self, umbral=0.15):
        grupos = []
        visitados = set()

        for i in range(len(self.sim_matrix)):
            if i in visitados:
                continue

            grupo = [i]
            visitados.add(i)

            for j in range(i + 1, len(self.sim_matrix)):
                if j not in visitados and self.sim_matrix[i][j] >= umbral:
                    grupo.append(j)
                    visitados.add(j)

            grupos.append(grupo)

        return grupos


pipeline = PipelineNLP()

for noticia in noticias:
    texto_completo = f"{noticia['titulo']}. {noticia['cuerpo']}"
    noticia["nlp"] = pipeline.procesar(texto_completo)


print("=== FASE 2.2: Representación Vectorial TF-IDF ===\n")

textos_para_vectorizar = [
    " ".join(noticia["nlp"]["sin_stopwords"])
    for noticia in noticias
]

representacion = RepresentacionVectorial()
representacion.construir_matriz(textos_para_vectorizar)

info = representacion.info_matriz()

print(f"Matriz TF-IDF: {info['documentos']} docs × {info['features']} features")
print(f"Densidad: {info['densidad']:.4f}")
print(f"Términos promedio por documento: {info['terminos_promedio_doc']:.1f}")

print(f"\nVocabulario muestra: {list(representacion.vocabulario()[:15])}")

print("\nTérminos más relevantes por noticia:")
for i, noticia in enumerate(noticias):
    print(f"\n[{noticia['categoria_original']}] {noticia['titulo']}")
    top = representacion.top_terminos_documento(i, n=5)

    for termino, peso in top:
        print(f"  {termino:<25} = {peso:.4f}")


print("\n=== FASE 2.3: Similitud entre Noticias ===\n")

calculador = CalculadorSimilitud(representacion.matriz)

print("Matriz de similitud coseno:")
print(f"{'':>5}", end="")

for i in range(len(noticias)):
    print(f"{'N' + str(i + 1):>7}", end="")

print()

for i in range(len(noticias)):
    print(f"N{i + 1:>3}", end=" ")

    for j in range(len(noticias)):
        print(f"{calculador.similitud_par(i, j):>7.3f}", end="")

    print()

print("\nNoticias más similares entre sí:")
for i, noticia in enumerate(noticias):
    similares = calculador.documentos_similares(i, top_n=1)

    if similares:
        j, sim = similares[0]

        if sim > 0.05:
            print(f"N{i + 1} ↔ N{j + 1} (sim={sim:.3f})")
            print(f"  {noticia['titulo']}")
            print(f"  {noticias[j]['titulo']}")
            print()

print("Grupos temáticos detectados:")
grupos = calculador.agrupar_por_similitud(umbral=0.1)

for g_idx, grupo in enumerate(grupos):
    print(f"Grupo {g_idx + 1}: {['N' + str(i + 1) for i in grupo]}")

    for i in grupo:
        print(f"  - {noticias[i]['titulo']}")