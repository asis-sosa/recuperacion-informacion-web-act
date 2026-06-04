import random
import numpy as np
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La nueva plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "categoria_original": "politica"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio sobre el calentamiento global y sus efectos.",
        "categoria_original": "ciencia"
    }
]


class SistemaRecomendacion:
    def __init__(self, noticias, matriz_similitud):
        self.noticias = noticias
        self.sim_matrix = matriz_similitud

    def recomendar(self, noticia_idx, top_n=2, excluir_misma_cat=False):
        similitudes = self.sim_matrix[noticia_idx]
        candidatos = []

        for i, sim in enumerate(similitudes):
            if i == noticia_idx:
                continue

            if excluir_misma_cat and self.noticias[i]["categoria_original"] == self.noticias[noticia_idx]["categoria_original"]:
                continue

            candidatos.append((i, sim))

        candidatos.sort(key=lambda x: -x[1])
        return candidatos[:top_n]

    def recomendar_por_perfil(self, indices_leidos, top_n=3):
        sim_acumulada = np.zeros(len(self.noticias))

        for idx in indices_leidos:
            sim_acumulada += self.sim_matrix[idx]

        for idx in indices_leidos:
            sim_acumulada[idx] = 0

        mejores = sim_acumulada.argsort()[::-1][:top_n]
        return [(i, sim_acumulada[i]) for i in mejores if sim_acumulada[i] > 0]


class DetectorTemasPublicidad:
    def __init__(self):
        self.mensajes = []

        self.catalogo_publicidad = {
            "tecnologia": [
                "Curso de IA y Machine Learning - 50% descuento",
                "Laptop para programadores - i9 + 32GB RAM",
                "Conferencia Tech 2026 - Boletos disponibles",
            ],
            "economia": [
                "App de inversiones - Comienza con $100",
                "Curso de finanzas personales gratuito",
                "Tarjeta de crédito sin anualidad",
            ],
            "ciencia": [
                "Suscripción a revista científica digital",
                "Telescopio astronómico - envío gratis",
                "Curso de ciencia de datos online",
            ],
            "politica": [
                "Portal de transparencia gubernamental",
                "Notificaciones de cambios legislativos",
                "Foro de participación ciudadana",
            ],
        }

        self._construir_perfiles()

    def _construir_perfiles(self):
        temas_texto = {
            "tecnologia": "inteligencia artificial programación software apps tecnología computadora robot digital innovación",
            "economia": "dinero inversión mercado bolsa finanzas banco economía empleo trabajo",
            "ciencia": "investigación científico descubrimiento estudio laboratorio clima universo",
            "politica": "gobierno elecciones presidente ley congreso partido democracia",
        }

        self.temas = list(temas_texto.keys())
        self.vec_temas = TfidfVectorizer()
        self.matriz_temas = self.vec_temas.fit_transform(temas_texto.values())

    def agregar_mensaje(self, usuario, texto):
        self.mensajes.append({
            "usuario": usuario,
            "texto": texto
        })

    def detectar_tema(self, ventana=5):
        if not self.mensajes:
            return "general", 0.0

        ultimos = self.mensajes[-ventana:]
        texto_ventana = " ".join(m["texto"] for m in ultimos)

        vec_conversacion = self.vec_temas.transform([texto_ventana])
        similitudes = cosine_similarity(vec_conversacion, self.matriz_temas)[0]

        mejor_idx = similitudes.argmax()

        return self.temas[mejor_idx], similitudes[mejor_idx]

    def obtener_publicidad(self, tema):
        if tema in self.catalogo_publicidad:
            return random.choice(self.catalogo_publicidad[tema])

        return "Descubre las mejores ofertas del día"

    def simular_chat(self, conversacion):
        resultados = []

        for usuario, mensaje in conversacion:
            self.agregar_mensaje(usuario, mensaje)
            tema, confianza = self.detectar_tema()
            publicidad = self.obtener_publicidad(tema)

            resultados.append({
                "usuario": usuario,
                "mensaje": mensaje,
                "tema": tema,
                "confianza": confianza,
                "publicidad": publicidad
            })

        return resultados


print("=== FASE 3.3: Sistema de Recomendación ===\n")

textos_noticias = [
    f"{n['titulo']} {n['cuerpo']}"
    for n in noticias
]

vectorizador = TfidfVectorizer()
matriz_tfidf = vectorizador.fit_transform(textos_noticias)
matriz_similitud = cosine_similarity(matriz_tfidf)

recomendador = SistemaRecomendacion(noticias, matriz_similitud)

print("Si leíste esta noticia, te recomendamos:")

for i in range(len(noticias)):
    recomendaciones = recomendador.recomendar(i, top_n=2)

    print(f"\nLeíste: {noticias[i]['titulo']}")

    for j, sim in recomendaciones:
        print(f"  → [{sim:.3f}] {noticias[j]['titulo']}")

print("\nRecomendación por perfil:")
print("Perfil simulado: usuario leyó la noticia 1 y la noticia 2")

perfil_recs = recomendador.recomendar_por_perfil([0, 1], top_n=3)

for idx, score in perfil_recs:
    print(f"  → [{score:.3f}] {noticias[idx]['titulo']}")


print("\n=== FASE 3.4: Detección de Temas + Publicidad ===\n")

detector = DetectorTemasPublicidad()

conversacion_usuarios = [
    ("Laura", "¿Vieron la noticia sobre la nueva IA de Google?"),
    ("Miguel", "Sí, dicen que puede programar mejor que muchos desarrolladores"),
    ("Laura", "Me preocupa el futuro del trabajo en tecnología"),
    ("Roberto", "Yo creo que es una oportunidad, hay que aprender machine learning"),
    ("Miguel", "Cambiando de tema, ¿cómo ven la economía este trimestre?"),
    ("Laura", "Los mercados están muy volátiles, mis inversiones bajaron"),
    ("Roberto", "El banco central anunció que subirá las tasas de interés"),
    ("Miguel", "Mejor hay que diversificar, quizá invertir en fondos indexados"),
]

resultados_chat = detector.simular_chat(conversacion_usuarios)

print("Simulación de chat con publicidad dirigida:")
print("-" * 65)

for r in resultados_chat:
    print(f"[{r['usuario']}]: {r['mensaje']}")
    print(f"  Tema: {r['tema'].upper()} | Confianza: {r['confianza']:.3f}")
    print(f"  Ad: {r['publicidad']}")
    print()

print("-" * 65)

temas_conv = Counter(r["tema"] for r in resultados_chat)
print(f"Resumen de temas en la conversación: {dict(temas_conv)}")