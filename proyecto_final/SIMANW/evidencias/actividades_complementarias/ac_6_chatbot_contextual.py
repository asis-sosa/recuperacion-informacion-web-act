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

motor = MotorBusqueda()
motor.indexar(noticias)

class ChatbotContextual:
    """
    AC-6: Chatbot con memoria de contexto.
    Las respuestas se enriquecen con el historial de la conversación.
    """

    def __init__(self, noticias, motor_busqueda):
        self.noticias = noticias
        self.motor = motor_busqueda
        self.historial = []
        self.contexto_temas = Counter()
        self.usuario_preferencias = {}

    def actualizar_contexto(self, pregunta, respuesta_tipo):
        """Actualiza el contexto basándose en la interacción."""
        self.historial.append({'pregunta': pregunta, 'tipo': respuesta_tipo})
        palabras_clave = pregunta.lower().split()
        for p in palabras_clave:
            if p in ['tecnología', 'ia', 'python', 'programación', 'software']:
                self.contexto_temas['tecnologia'] += 1
            elif p in ['economía', 'mercado', 'finanzas', 'dinero']:
                self.contexto_temas['economia'] += 1
            elif p in ['ciencia', 'clima', 'investigación']:
                self.contexto_temas['ciencia'] += 1

    def responder(self, pregunta):
        """Genera respuesta considerando el contexto previo."""
        pregunta_lower = pregunta.lower()

        # Detectar referencias al contexto
        if any(ref in pregunta_lower for ref in ['eso', 'esa', 'anterior', 'más sobre', 'otra']):
            if self.historial:
                ultimo = self.historial[-1]
                pregunta_expandida = f"{ultimo['pregunta']} {pregunta}"
                resultados = self.motor.buscar_vectorial(pregunta_expandida, top_k=2)
                if resultados:
                    tipo = 'contextual'
                    resp = f"Basándome en nuestra conversación anterior, encontré: {resultados[0]['titulo']}"
                    self.actualizar_contexto(pregunta, tipo)
                    return resp, tipo, resultados[0]['relevancia']

        # Respuesta con sesgo hacia temas de interés del usuario
        resultados = self.motor.buscar_vectorial(pregunta, top_k=5)
        if resultados:
            # Priorizar resultados en categorías que le interesan al usuario
            if self.contexto_temas:
                tema_favorito = self.contexto_temas.most_common(1)[0][0]
                for r in resultados:
                    if r['categoria'] == tema_favorito:
                        tipo = 'personalizada'
                        resp = f"Como te interesa {tema_favorito}, mira esto: {r['titulo']}"
                        self.actualizar_contexto(pregunta, tipo)
                        return resp, tipo, r['relevancia']

            tipo = 'directa'
            resp = f"{resultados[0]['titulo']}. {resultados[0]['snippet']}"
            self.actualizar_contexto(pregunta, tipo)
            return resp, tipo, resultados[0]['relevancia']

        tipo = 'fallback'
        resp = "No encontré algo específico. ¿Puedes darme más detalles?"
        self.actualizar_contexto(pregunta, tipo)
        return resp, tipo, 0.0

    def estadisticas_sesion(self):
        return {
            'interacciones': len(self.historial),
            'temas_interes': dict(self.contexto_temas.most_common()),
            'tipos_respuesta': Counter(h['tipo'] for h in self.historial)
        }


chatbot_ctx = ChatbotContextual(noticias, motor)

print("=== AC-6: Chatbot con Memoria de Contexto ===\n")

conversacion_sesion = [
    "¿Qué noticias hay de tecnología?",
    "Cuéntame más sobre eso",
    "¿Hay algo sobre inteligencia artificial?",
    "¿Y algo de economía?",
    "Dame otra noticia similar a la anterior",
]

for pregunta in conversacion_sesion:
    respuesta, tipo, confianza = chatbot_ctx.responder(pregunta)
    print(f"  Usuario: {pregunta}")
    print(f"  Bot [{tipo}][{confianza:.2f}]: {respuesta[:80]}...")
    print()

stats = chatbot_ctx.estadisticas_sesion()
print(f"Estadísticas de sesión:")
print(f"  Interacciones: {stats['interacciones']}")
print(f"  Temas de interés: {stats['temas_interes']}")
print(f"  Tipos de respuesta: {dict(stats['tipos_respuesta'])}")