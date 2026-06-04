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
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "categoria_original": "gobierno",
        "categoria_predicha": "politica",
        "sentimiento": {"etiqueta": "neutral"}
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo"}
    }
]


class ChatbotSIMANW:
    def __init__(self, noticias):
        self.noticias = noticias
        self.historial = []
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=2000)
        self._construir_base()

    def _construir_base(self):
        self.pares_qa = []

        for n in self.noticias:
            titulo = n["titulo"]
            cuerpo = n["cuerpo"]
            cat = n.get("categoria_predicha", n.get("categoria_original", ""))
            sent = n.get("sentimiento", {}).get("etiqueta", "")

            self.pares_qa.append({
                "contexto": f"{titulo} {cuerpo}",
                "respuesta": f"{titulo}. {cuerpo}",
                "tipo": "contenido"
            })

            self.pares_qa.append({
                "contexto": f"categoría tema tipo {cat} {titulo}",
                "respuesta": f"Esa noticia pertenece a la categoría '{cat}': {titulo}",
                "tipo": "categoria"
            })

            self.pares_qa.append({
                "contexto": f"sentimiento opinión tono {sent} {titulo}",
                "respuesta": f"El tono de esa noticia es {sent}: {titulo}",
                "tipo": "sentimiento"
            })

        contextos = [p["contexto"] for p in self.pares_qa]
        self.matriz_qa = self.vectorizer.fit_transform(contextos)

    def responder(self, pregunta, umbral=0.05):
        pregunta_vec = self.vectorizer.transform([pregunta])
        similitudes = cosine_similarity(pregunta_vec, self.matriz_qa)[0]

        mejor_idx = similitudes.argmax()
        confianza = similitudes[mejor_idx]

        self.historial.append({
            "pregunta": pregunta,
            "confianza": confianza
        })

        if confianza < umbral:
            return "No tengo información suficiente para responder eso. ¿Puedes reformular tu pregunta?", 0.0

        return self.pares_qa[mejor_idx]["respuesta"], confianza

    def resumen_interaccion(self):
        n = len(self.historial)

        if n == 0:
            return "Sin interacciones"

        promedio = sum(h["confianza"] for h in self.historial) / n

        return f"{n} preguntas, confianza promedio: {promedio:.3f}"


chatbot = ChatbotSIMANW(noticias)

print("=== FASE 5.1: Chatbot del SIMANW ===\n")

preguntas_usuario = [
    "¿Qué noticias hay sobre inteligencia artificial?",
    "¿Cuál es el tono de la noticia de los mercados financieros?",
    "¿Hay algo sobre datos abiertos del gobierno?",
    "¿Qué noticias de tecnología tienen sentimiento positivo?",
    "¿Cuál es la capital de Francia?",
]

for pregunta in preguntas_usuario:
    respuesta, confianza = chatbot.responder(pregunta)

    print(f"Usuario: {pregunta}")
    print(f"Bot [{confianza:.3f}]: {respuesta}")
    print()

print(f"Resumen: {chatbot.resumen_interaccion()}")