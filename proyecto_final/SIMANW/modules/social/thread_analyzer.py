from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re


class AnalizadorHiloDiscusion:
    def __init__(self):
        self.mensajes = []
        self.positivas = {
            "amazing", "agree", "exciting", "great", "best",
            "excelente", "positivo", "mejora", "bueno", "oportunidad"
        }
        self.negativas = {
            "worries", "terrible", "concern", "lost", "bad",
            "preocupa", "negativo", "malo", "riesgo", "crisis"
        }

    def sentimiento_simple(self, texto):
        texto = texto.lower()
        pos = sum(1 for p in self.positivas if p in texto)
        neg = sum(1 for n in self.negativas if n in texto)

        if pos > neg:
            return 0.6
        if neg > pos:
            return -0.6
        return 0.0

    def cargar_hilo(self, mensajes):
        self.mensajes = mensajes

        for msg in self.mensajes:
            msg["sentimiento"] = self.sentimiento_simple(msg["texto"])

    def evolucion_sentimiento(self, ventana=3):
        sentimientos = [m["sentimiento"] for m in self.mensajes]
        evolucion = []

        for i in range(len(sentimientos)):
            inicio = max(0, i - ventana + 1)
            promedio = sum(sentimientos[inicio:i + 1]) / (i - inicio + 1)

            evolucion.append({
                "posicion": i + 1,
                "sentimiento_puntual": sentimientos[i],
                "tendencia": promedio
            })

        return evolucion

    def detectar_subtemas(self, n_clusters=3):
        textos = [m["texto"] for m in self.mensajes]

        if len(textos) < 2:
            return {}

        vectorizer = TfidfVectorizer(max_features=500)
        X = vectorizer.fit_transform(textos)

        n_clusters = min(n_clusters, len(textos))
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = km.fit_predict(X)

        subtemas = defaultdict(list)

        for i, cluster_id in enumerate(clusters):
            subtemas[cluster_id].append(i)

        terminos = vectorizer.get_feature_names_out()
        subtemas_info = {}

        for cluster_id, indices in subtemas.items():
            centroide = km.cluster_centers_[cluster_id]
            top_idx = centroide.argsort()[-5:][::-1]
            keywords = [terminos[j] for j in top_idx]

            subtemas_info[cluster_id] = {
                "keywords": keywords,
                "n_mensajes": len(indices),
                "mensajes_idx": indices
            }

        return subtemas_info

    def usuarios_mas_activos(self, top_n=5):
        participacion = Counter(m["usuario"] for m in self.mensajes)
        return participacion.most_common(top_n)

    def resumen_hilo(self):
        total = len(self.mensajes)

        if total == 0:
            return {}

        promedio = sum(m["sentimiento"] for m in self.mensajes) / total
        positivos = sum(1 for m in self.mensajes if m["sentimiento"] > 0.05)
        negativos = sum(1 for m in self.mensajes if m["sentimiento"] < -0.05)

        hashtags = Counter()

        for m in self.mensajes:
            tags = re.findall(r"#(\w+)", m["texto"])
            hashtags.update(tags)

        return {
            "total_mensajes": total,
            "participantes": len(set(m["usuario"] for m in self.mensajes)),
            "sentimiento_promedio": promedio,
            "tono": "positivo" if promedio > 0.05 else "negativo" if promedio < -0.05 else "mixto",
            "positivos_pct": 100 * positivos / total,
            "negativos_pct": 100 * negativos / total,
            "hashtags_top": hashtags.most_common(5),
            "usuarios_activos": self.usuarios_mas_activos(3)
        }


def hilo_demo():
    return [
        {"usuario": "@dev_laura", "texto": "La nueva IA para programar es excelente #AI", "timestamp": "10:00"},
        {"usuario": "@tech_mike", "texto": "Estoy de acuerdo, mejora mucho el desarrollo de software #AI", "timestamp": "10:05"},
        {"usuario": "@skeptic_joe", "texto": "Me preocupa que pueda afectar empleos", "timestamp": "10:08"},
        {"usuario": "@data_sara", "texto": "El problema real son los datos sesgados y la ética #AIethics", "timestamp": "10:15"},
        {"usuario": "@tech_mike", "texto": "Aun así es una gran oportunidad para innovar", "timestamp": "10:20"},
        {"usuario": "@skeptic_joe", "texto": "Perdí un trabajo freelance por herramientas de IA, es terrible", "timestamp": "10:25"},
        {"usuario": "@prof_chen", "texto": "La regulación y la capacitación son necesarias", "timestamp": "10:30"},
        {"usuario": "@dev_laura", "texto": "El desarrollo responsable de IA es clave #responsible", "timestamp": "10:40"},
    ]