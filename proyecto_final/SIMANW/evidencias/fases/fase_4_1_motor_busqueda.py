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
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
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
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "categoria_original": "gobierno",
        "categoria_predicha": "politica",
        "sentimiento": {"etiqueta": "neutral"}
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio sobre el calentamiento global.",
        "categoria_original": "ciencia",
        "categoria_predicha": "ciencia",
        "sentimiento": {"etiqueta": "negativo"}
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

    def buscar_booleana(self, consulta, modo="AND"):
        terminos = consulta.lower().split()

        if not terminos:
            return []

        if modo == "AND":
            resultado = set(self.indice_invertido.get(terminos[0], {}).keys())

            for termino in terminos[1:]:
                resultado &= set(self.indice_invertido.get(termino, {}).keys())

        else:
            resultado = set()

            for termino in terminos:
                resultado |= set(self.indice_invertido.get(termino, {}).keys())

        return list(resultado)

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

    def info_indice(self):
        return {
            "documentos_indexados": self.N,
            "terminos_en_indice": len(self.indice_invertido),
            "tamano_promedio_posting": sum(len(v) for v in self.indice_invertido.values()) / max(len(self.indice_invertido), 1)
        }


motor = MotorBusqueda()
motor.indexar(noticias)

print("=== FASE 4.1: Motor de Búsqueda ===\n")

info = motor.info_indice()

print("Índice construido:")
print(f"  Documentos: {info['documentos_indexados']}")
print(f"  Términos únicos: {info['terminos_en_indice']}")
print(f"  Postings promedio: {info['tamano_promedio_posting']:.2f}")

consultas = [
    "inteligencia artificial tecnología",
    "mercados financieros economía",
    "datos abiertos gobierno semántica",
    "Python programación desarrollo",
    "cambio climático investigación científica",
]

print("\n--- Resultados de Búsqueda Vectorial ---")

for consulta in consultas:
    resultados = motor.buscar_vectorial(consulta, top_k=2)

    print(f"\nConsulta: '{consulta}'")

    if not resultados:
        print("  Sin resultados relevantes.")

    for r in resultados:
        print(f"  [{r['relevancia']:.3f}] {r['titulo']}")
        print(f"    Cat: {r['categoria']} | Sent: {r['sentimiento']}")
        print(f"    Snippet: {r['snippet']}")


print("\n--- Búsqueda Booleana de Prueba ---")

consulta_bool = "inteligencia artificial"
resultados_and = motor.buscar_booleana(consulta_bool, modo="AND")
resultados_or = motor.buscar_booleana(consulta_bool, modo="OR")

print(f"Consulta booleana: '{consulta_bool}'")
print(f"AND: {resultados_and}")
print(f"OR: {resultados_or}")