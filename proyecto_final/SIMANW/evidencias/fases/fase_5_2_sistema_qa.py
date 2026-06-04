from collections import Counter, defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.45}
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación.",
        "categoria_original": "economia",
        "categoria_predicha": "economia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.35}
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.38}
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "categoria_original": "gobierno",
        "categoria_predicha": "politica",
        "sentimiento": {"etiqueta": "neutral", "compound": 0.0}
    }
]


class MotorBusqueda:
    def __init__(self):
        self.documentos = {}
        self.indice_invertido = defaultdict(dict)
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.matriz_busqueda = None

    def indexar(self, documentos):
        textos = []

        for doc_id, doc in enumerate(documentos):
            self.documentos[doc_id] = doc
            texto = f"{doc['titulo']} {doc['cuerpo']}"
            textos.append(texto)

            tokens = texto.lower().split()
            tf = Counter(tokens)

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
                    "snippet": self.documentos[idx]["cuerpo"][:100] + "..."
                })

        return resultados


class SistemaQA:
    def __init__(self, noticias, motor_busqueda):
        self.noticias = noticias
        self.motor = motor_busqueda
        self.historial_conversacion = []

    def clasificar_intencion(self, pregunta):
        pregunta_lower = pregunta.lower()

        if any(w in pregunta_lower for w in ["cuántas", "cuantas", "total", "número"]):
            return "conteo"

        elif any(w in pregunta_lower for w in ["resumen", "resume", "sintetiza"]):
            return "resumen"

        elif any(w in pregunta_lower for w in ["sentimiento", "tono", "opinión", "positiv", "negativ"]):
            return "sentimiento"

        elif any(w in pregunta_lower for w in ["categoría", "categoria", "tema", "tipo", "clasifica"]):
            return "categoria"

        elif any(w in pregunta_lower for w in ["compara", "diferencia", "relación"]):
            return "comparacion"

        elif any(w in pregunta_lower for w in ["recomienda", "sugiere", "similar"]):
            return "recomendacion"

        else:
            return "busqueda"

    def generar_respuesta(self, pregunta):
        intencion = self.clasificar_intencion(pregunta)

        if intencion == "conteo":
            return self._respuesta_conteo()

        elif intencion == "sentimiento":
            return self._respuesta_sentimiento()

        elif intencion == "categoria":
            return self._respuesta_categoria()

        elif intencion == "resumen":
            return self._respuesta_resumen()

        elif intencion == "recomendacion":
            return self._respuesta_recomendacion(pregunta)

        else:
            return self._respuesta_busqueda(pregunta)

    def _respuesta_conteo(self):
        cats = Counter(
            n.get("categoria_predicha", n["categoria_original"])
            for n in self.noticias
        )

        respuesta = f"Tengo {len(self.noticias)} noticias indexadas. "
        respuesta += "Distribución: "
        respuesta += ", ".join(f"{categoria}: {cantidad}" for categoria, cantidad in cats.most_common())

        return respuesta, "conteo", 1.0

    def _respuesta_sentimiento(self):
        noticias_con_sentimiento = [
            n for n in self.noticias
            if "sentimiento" in n
        ]

        sentimientos = Counter(
            n["sentimiento"]["etiqueta"]
            for n in noticias_con_sentimiento
        )

        promedio = sum(
            n["sentimiento"]["compound"]
            for n in noticias_con_sentimiento
        ) / max(len(noticias_con_sentimiento), 1)

        tono_general = (
            "positivo" if promedio > 0.05
            else "negativo" if promedio < -0.05
            else "neutral"
        )

        respuesta = f"Análisis de sentimiento: {dict(sentimientos)}. "
        respuesta += f"El tono general es {tono_general} "
        respuesta += f"(promedio: {promedio:+.3f})."

        return respuesta, "sentimiento", 0.9

    def _respuesta_categoria(self):
        cats = Counter(
            n.get("categoria_predicha", n["categoria_original"])
            for n in self.noticias
        )

        respuesta = "Categorías detectadas en las noticias:\n"

        for categoria, cantidad in cats.most_common():
            ejemplos = [
                n["titulo"][:50]
                for n in self.noticias
                if n.get("categoria_predicha", n["categoria_original"]) == categoria
            ]

            respuesta += f"- {categoria} ({cantidad}): {ejemplos[0]}...\n"

        return respuesta, "categoria", 0.9

    def _respuesta_resumen(self):
        respuesta = f"Resumen del corpus ({len(self.noticias)} noticias):\n"

        for n in self.noticias:
            sent = n.get("sentimiento", {}).get("etiqueta", "?")
            cat = n.get("categoria_predicha", n["categoria_original"])

            respuesta += f"- [{cat}][{sent}] {n['titulo'][:60]}\n"

        return respuesta, "resumen", 1.0

    def _respuesta_recomendacion(self, pregunta):
        resultados = self.motor.buscar_vectorial(pregunta, top_k=3)

        if resultados:
            respuesta = "Te recomiendo estas noticias relacionadas:\n"

            for r in resultados:
                respuesta += f"- [{r['relevancia']:.2f}] {r['titulo'][:60]}...\n"

            return respuesta, "recomendacion", resultados[0]["relevancia"]

        return "No encontré noticias para recomendar sobre ese tema.", "recomendacion", 0.0

    def _respuesta_busqueda(self, pregunta):
        resultados = self.motor.buscar_vectorial(pregunta, top_k=2)

        if resultados:
            mejor = resultados[0]
            respuesta = f"{mejor['titulo']}.\n{mejor['snippet']}"
            return respuesta, "busqueda", mejor["relevancia"]

        return "No encontré información relevante para tu pregunta.", "busqueda", 0.0

    def conversar(self, pregunta):
        respuesta, tipo, confianza = self.generar_respuesta(pregunta)

        self.historial_conversacion.append({
            "pregunta": pregunta,
            "tipo": tipo,
            "confianza": confianza
        })

        return respuesta, tipo, confianza


motor = MotorBusqueda()
motor.indexar(noticias)

qa_system = SistemaQA(noticias, motor)

print("=== FASE 5.2: Sistema Question/Answering ===\n")

preguntas_qa = [
    "¿Cuántas noticias tienes?",
    "¿Cuál es el sentimiento general de las noticias?",
    "¿Qué categorías de noticias hay?",
    "Dame un resumen de las noticias",
    "Recomiéndame algo sobre tecnología",
    "¿Qué dice la noticia sobre Python?",
]

for pregunta in preguntas_qa:
    respuesta, tipo, confianza = qa_system.conversar(pregunta)

    print(f"Pregunta: {pregunta}")
    print(f"[{tipo}][{confianza:.2f}]")
    print(respuesta)
    print()