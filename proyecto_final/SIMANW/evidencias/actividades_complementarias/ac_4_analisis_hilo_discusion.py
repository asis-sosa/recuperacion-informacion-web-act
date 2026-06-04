from collections import Counter, defaultdict
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import nltk
import re

nltk.download("vader_lexicon", quiet=True)

class AnalizadorHiloDiscusion:
    """
    AC-4: Analiza un hilo completo de red social.
    El alumno debe aplicarlo a datos reales (Twitter/X, Reddit, foros).
    """

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.mensajes = []

    def cargar_hilo(self, mensajes):
        """Carga un hilo de discusión."""
        self.mensajes = mensajes
        for msg in self.mensajes:
            msg['sentimiento'] = self.sia.polarity_scores(msg['texto'])['compound']

    def evolucion_sentimiento(self, ventana=3):
        """Analiza cómo evoluciona el sentimiento a lo largo del hilo."""
        sentimientos = [m['sentimiento'] for m in self.mensajes]
        evolucion = []
        for i in range(len(sentimientos)):
            inicio = max(0, i - ventana + 1)
            promedio_ventana = sum(sentimientos[inicio:i+1]) / (i - inicio + 1)
            evolucion.append({
                'posicion': i + 1,
                'sentimiento_puntual': sentimientos[i],
                'tendencia': promedio_ventana
            })
        return evolucion

    def detectar_subtemas(self, n_clusters=3):
        """Detecta subtemas en el hilo usando clustering."""
        textos = [m['texto'] for m in self.mensajes]
        vec = TfidfVectorizer(max_features=500, stop_words='english')
        X = vec.fit_transform(textos)

        n_clusters = min(n_clusters, len(textos))
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = km.fit_predict(X)

        subtemas = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            subtemas[cluster_id].append(i)

        # Extraer palabras clave de cada subtema
        terminos = vec.get_feature_names_out()
        subtemas_info = {}
        for cluster_id, indices in subtemas.items():
            centroide = km.cluster_centers_[cluster_id]
            top_idx = centroide.argsort()[-5:][::-1]
            keywords = [terminos[j] for j in top_idx]
            subtemas_info[cluster_id] = {
                'keywords': keywords,
                'n_mensajes': len(indices),
                'mensajes_idx': indices
            }

        return subtemas_info

    def usuarios_mas_activos(self, top_n=5):
        """Identifica usuarios más participativos."""
        participacion = Counter(m['usuario'] for m in self.mensajes)
        return participacion.most_common(top_n)

    def resumen_hilo(self):
        """Genera resumen automático del hilo."""
        total = len(self.mensajes)
        sent_promedio = sum(m['sentimiento'] for m in self.mensajes) / total
        positivos = sum(1 for m in self.mensajes if m['sentimiento'] > 0.05)
        negativos = sum(1 for m in self.mensajes if m['sentimiento'] < -0.05)

        hashtags = Counter()
        for m in self.mensajes:
            tags = re.findall(r'#(\w+)', m['texto'])
            hashtags.update(tags)

        return {
            'total_mensajes': total,
            'participantes': len(set(m['usuario'] for m in self.mensajes)),
            'sentimiento_promedio': sent_promedio,
            'tono': 'positivo' if sent_promedio > 0.05 else 'negativo' if sent_promedio < -0.05 else 'mixto',
            'positivos_pct': 100 * positivos / total,
            'negativos_pct': 100 * negativos / total,
            'hashtags_top': hashtags.most_common(5),
            'usuarios_activos': self.usuarios_mas_activos(3),
        }


# Simular un hilo de discusión sobre IA
hilo_ia = [
    {"usuario": "@dev_laura", "texto": "Just tried the new AI coding assistant and it's amazing! #AI #coding",
     "timestamp": "10:00"},
    {"usuario": "@tech_mike", "texto": "I agree, the code suggestions are incredibly accurate #AI",
     "timestamp": "10:05"},
    {"usuario": "@skeptic_joe", "texto": "But what about job displacement? This AI thing worries me a lot",
     "timestamp": "10:08"},
    {"usuario": "@dev_laura", "texto": "Good point Joe, but I think it's a tool not a replacement #AItools",
     "timestamp": "10:12"},
    {"usuario": "@data_sara", "texto": "The real concern is bias in training data, we need better datasets",
     "timestamp": "10:15"},
    {"usuario": "@tech_mike", "texto": "True, but the progress is undeniable. Exciting times! #innovation",
     "timestamp": "10:20"},
    {"usuario": "@skeptic_joe", "texto": "I lost my freelance gig because of AI. This is terrible for workers",
     "timestamp": "10:25"},
    {"usuario": "@prof_chen", "texto": "Research shows AI creates more jobs than it destroys historically",
     "timestamp": "10:30"},
    {"usuario": "@data_sara", "texto": "We need regulation and ethical guidelines urgently #AIethics",
     "timestamp": "10:35"},
    {"usuario": "@dev_laura", "texto": "Totally agree with Sara. Responsible AI development is key #responsible",
     "timestamp": "10:40"},
    {"usuario": "@tech_mike", "texto": "Companies investing in AI training for employees is the best approach",
     "timestamp": "10:45"},
    {"usuario": "@prof_chen", "texto": "Great discussion everyone! The future needs both innovation and responsibility",
     "timestamp": "10:50"},
]

analizador_hilo = AnalizadorHiloDiscusion()
analizador_hilo.cargar_hilo(hilo_ia)

print("=== AC-4: Análisis de Hilo de Discusión ===\n")

# Resumen
resumen = analizador_hilo.resumen_hilo()
print("--- Resumen del Hilo ---")
print(f"  Mensajes: {resumen['total_mensajes']}")
print(f"  Participantes: {resumen['participantes']}")
print(f"  Tono general: {resumen['tono']} ({resumen['sentimiento_promedio']:+.3f})")
print(f"  Positivos: {resumen['positivos_pct']:.0f}% | Negativos: {resumen['negativos_pct']:.0f}%")
print(f"  Hashtags: {resumen['hashtags_top']}")
print(f"  Más activos: {resumen['usuarios_activos']}")

# Evolución del sentimiento
print("\n--- Evolución del Sentimiento ---")
evolucion = analizador_hilo.evolucion_sentimiento(ventana=3)
for e in evolucion:
    barra = "+" * int(max(0, e['tendencia'] * 10)) + "-" * int(max(0, -e['tendencia'] * 10))
    print(f"  Msg {e['posicion']:>2}: [{e['sentimiento_puntual']:+.2f}] tendencia: {e['tendencia']:+.3f} |{barra}")

# Subtemas
print("\n--- Subtemas Detectados ---")
subtemas = analizador_hilo.detectar_subtemas(n_clusters=3)
for cluster_id, info in subtemas.items():
    print(f"  Subtema {cluster_id+1} ({info['n_mensajes']} msgs): {info['keywords']}")