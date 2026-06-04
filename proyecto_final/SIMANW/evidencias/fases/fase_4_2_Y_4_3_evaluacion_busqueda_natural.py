from collections import Counter, defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo"}
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación.",
        "categoria_original": "economia",
        "categoria_predicha": "economia",
        "sentimiento": {"etiqueta": "negativo"}
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo"}
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio preocupante sobre el calentamiento global.",
        "categoria_original": "ciencia",
        "categoria_predicha": "ciencia",
        "sentimiento": {"etiqueta": "negativo"}
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "categoria_original": "gobierno",
        "categoria_predicha": "politica",
        "sentimiento": {"etiqueta": "neutral"}
    }
]


class MotorBusqueda:
    def __init__(self):
        self.documentos = {}
        self.indice_invertido = defaultdict(dict)
        self.doc_lengths = {}
        self.N = 0
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.matriz_busqueda = None

    def indexar(self, documentos):
        self.N = len(documentos)
        textos = []

        for doc_id, doc in enumerate(documentos):
            self.documentos[doc_id] = doc
            texto = f"{doc['titulo']} {doc['cuerpo']}"
            textos.append(texto)

            tokens = texto.lower().split()
            tf = Counter(tokens)
            self.doc_lengths[doc_id] = len(tokens)

            for term, freq in tf.items():
                self.indice_invertido[term][doc_id] = freq

        self.matriz_busqueda = self.vectorizer.fit_transform(textos)

    def buscar_vectorial(self, consulta, top_k=5):
        consulta_vec = self.vectorizer.transform([consulta])
        similitudes = cosine_similarity(consulta_vec, self.matriz_busqueda)[0]
        indices = similitudes.argsort()[::-1][:top_k]

        resultados = []

        for idx in indices:
            if similitudes[idx] > 0:
                resultados.append({
                    "doc_id": idx,
                    "titulo": self.documentos[idx]["titulo"],
                    "relevancia": float(similitudes[idx]),
                    "categoria": self.documentos[idx].get(
                        "categoria_predicha",
                        self.documentos[idx].get("categoria_original", "?")
                    ),
                    "sentimiento": self.documentos[idx].get("sentimiento", {}).get("etiqueta", "?"),
                    "snippet": self.documentos[idx]["cuerpo"][:80] + "..."
                })

        return resultados


class EvaluadorIRS:
    @staticmethod
    def precision(recuperados, relevantes):
        recuperados = set(recuperados)
        relevantes = set(relevantes)
        tp = len(recuperados & relevantes)
        return tp / len(recuperados) if recuperados else 0

    @staticmethod
    def recall(recuperados, relevantes):
        recuperados = set(recuperados)
        relevantes = set(relevantes)
        tp = len(recuperados & relevantes)
        return tp / len(relevantes) if relevantes else 0

    @staticmethod
    def f1(precision, recall):
        if precision + recall == 0:
            return 0

        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def precision_at_k(ranking, relevantes, k):
        top_k = set(ranking[:k])
        relevantes = set(relevantes)
        return len(top_k & relevantes) / k

    @staticmethod
    def average_precision(ranking, relevantes):
        relevantes = set(relevantes)
        suma = 0
        relevantes_encontrados = 0

        for i, doc in enumerate(ranking, 1):
            if doc in relevantes:
                relevantes_encontrados += 1
                suma += relevantes_encontrados / i

        return suma / len(relevantes) if relevantes else 0

    def evaluar_consulta(self, recuperados_ids, relevantes_ids, total_docs):
        p = self.precision(recuperados_ids, relevantes_ids)
        r = self.recall(recuperados_ids, relevantes_ids)
        f = self.f1(p, r)
        ap = self.average_precision(recuperados_ids, relevantes_ids)

        return {
            "precision": p,
            "recall": r,
            "f1": f,
            "average_precision": ap
        }


class BusquedaNatural:
    def __init__(self, motor_busqueda):
        self.motor = motor_busqueda

    def interpretar_consulta(self, consulta_natural):
        consulta_natural = consulta_natural.lower()

        filtros = {
            "sentimiento": None,
            "categoria": None
        }

        if any(p in consulta_natural for p in ["buena", "positiva", "optimista"]):
            filtros["sentimiento"] = "positivo"

        elif any(p in consulta_natural for p in ["mala", "negativa", "pesimista", "preocupante"]):
            filtros["sentimiento"] = "negativo"

        categorias_map = {
            "tecnología": "tecnologia",
            "tech": "tecnologia",
            "computación": "tecnologia",
            "programación": "tecnologia",
            "python": "tecnologia",
            "economía": "economia",
            "mercados": "economia",
            "finanzas": "economia",
            "ciencia": "ciencia",
            "científico": "ciencia",
            "investigación": "ciencia",
            "clima": "ciencia",
            "gobierno": "politica",
            "política": "politica",
            "datos": "politica"
        }

        for keyword, cat in categorias_map.items():
            if keyword in consulta_natural:
                filtros["categoria"] = cat
                break

        return filtros

    def buscar_natural(self, consulta_natural, top_k=3):
        filtros = self.interpretar_consulta(consulta_natural)
        resultados = self.motor.buscar_vectorial(consulta_natural, top_k=top_k * 2)

        filtrados = []

        for r in resultados:
            if filtros["sentimiento"] and r["sentimiento"] != filtros["sentimiento"]:
                continue

            if filtros["categoria"] and r["categoria"] != filtros["categoria"]:
                continue

            filtrados.append(r)

        return filtrados[:top_k] if filtrados else resultados[:top_k]


motor = MotorBusqueda()
motor.indexar(noticias)


print("=== FASE 4.2: Evaluación del Motor de Búsqueda ===\n")

evaluador = EvaluadorIRS()

evaluaciones = [
    {
        "consulta": "inteligencia artificial",
        "relevantes": [0],
        "recuperados": [r["doc_id"] for r in motor.buscar_vectorial("inteligencia artificial", top_k=3)]
    },
    {
        "consulta": "economía mercados",
        "relevantes": [1],
        "recuperados": [r["doc_id"] for r in motor.buscar_vectorial("economía mercados", top_k=3)]
    },
    {
        "consulta": "datos gobierno",
        "relevantes": [4],
        "recuperados": [r["doc_id"] for r in motor.buscar_vectorial("datos gobierno", top_k=3)]
    }
]

print(f"{'Consulta':<25} {'Precision':>10} {'Recall':>10} {'F1':>10} {'AP':>10}")
print("-" * 67)

map_total = 0

for ev in evaluaciones:
    metricas = evaluador.evaluar_consulta(
        ev["recuperados"],
        ev["relevantes"],
        len(noticias)
    )

    map_total += metricas["average_precision"]

    print(
        f"{ev['consulta']:<25} "
        f"{metricas['precision']:>10.3f} "
        f"{metricas['recall']:>10.3f} "
        f"{metricas['f1']:>10.3f} "
        f"{metricas['average_precision']:>10.3f}"
    )

map_score = map_total / len(evaluaciones)

print(f"\nMAP (Mean Average Precision): {map_score:.3f}")

print("\n--- Precision@K para 'inteligencia artificial' ---")

ranking = [0, 2, 1, 3, 4]
relevantes = [0]

for k in range(1, 6):
    pk = evaluador.precision_at_k(ranking, relevantes, k)
    print(f"P@{k} = {pk:.3f}")


print("\n=== FASE 4.3: Búsqueda en Lenguaje Natural ===\n")

busqueda_nl = BusquedaNatural(motor)

consultas_naturales = [
    "Muéstrame noticias positivas sobre tecnología",
    "¿Qué noticias hay sobre datos del gobierno?",
    "Busco información preocupante sobre el clima",
    "¿Hay algo nuevo de programación en Python?",
]

for consulta in consultas_naturales:
    resultados = busqueda_nl.buscar_natural(consulta, top_k=2)

    print(f'Usuario: "{consulta}"')

    if resultados:
        for r in resultados:
            print(f"  → [{r['relevancia']:.3f}] {r['titulo']}")
            print(f"     Cat: {r['categoria']} | Sent: {r['sentimiento']}")
    else:
        print("  → Sin resultados relevantes")

    print()