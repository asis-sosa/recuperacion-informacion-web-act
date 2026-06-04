from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DetectorTemasPublicidad:
    def __init__(self):
        self.mensajes = []

        self.catalogo_publicidad = {
            "tecnologia": [
                "Curso de IA y Machine Learning",
                "Laptop para programadores",
                "Conferencia Tech 2026"
            ],
            "economia": [
                "Curso de finanzas personales",
                "App de inversiones",
                "Seminario de economía digital"
            ],
            "ciencia": [
                "Revista científica digital",
                "Curso de ciencia de datos",
                "Taller de investigación aplicada"
            ],
            "politica": [
                "Portal de transparencia ciudadana",
                "Foro de participación pública",
                "Boletín de cambios legislativos"
            ],
            "salud": [
                "Aplicación de seguimiento médico",
                "Curso de salud digital",
                "Programa de bienestar preventivo"
            ],
            "videojuegos": [
                "Curso de desarrollo de videojuegos",
                "Torneo eSports local",
                "Consola gamer en promoción"
            ]
        }

        self.temas_texto = {
            "tecnologia": "inteligencia artificial software programación python datos tecnología digital innovación",
            "economia": "dinero inversión mercado bolsa finanzas banco economía empleo exportaciones",
            "ciencia": "investigación científico descubrimiento laboratorio clima universo estudio",
            "politica": "gobierno elecciones ley congreso partido democracia datos abiertos",
            "salud": "hospital médico paciente tratamiento vacuna enfermedad salud diagnóstico",
            "videojuegos": "videojuego videojuegos gaming gamer consola esports nintendo xbox playstation"
        }

        self.temas = list(self.temas_texto.keys())
        self.vectorizer = TfidfVectorizer()
        self.matriz_temas = self.vectorizer.fit_transform(self.temas_texto.values())

    def agregar_mensaje(self, usuario, texto):
        self.mensajes.append({
            "usuario": usuario,
            "texto": texto
        })

    def detectar_tema(self, ventana=5):
        if not self.mensajes:
            return "general", 0.0

        ultimos = self.mensajes[-ventana:]
        texto = " ".join(m["texto"] for m in ultimos)

        vec = self.vectorizer.transform([texto])
        similitudes = cosine_similarity(vec, self.matriz_temas)[0]

        mejor_idx = similitudes.argmax()
        tema = self.temas[mejor_idx]
        confianza = float(similitudes[mejor_idx])

        return tema, confianza

    def obtener_publicidad(self, tema):
        anuncios = self.catalogo_publicidad.get(tema)

        if not anuncios:
            return "Explora nuevos contenidos recomendados."

        return anuncios[0]