from collections import Counter
import re


class AnalizadorSentimientos:
    def __init__(self):
        self.positivas = {
            "positivo", "positivos", "positiva", "positivas",
            "mejora", "mejoran", "mejorar", "mejoró",
            "beneficio", "beneficios", "excelente", "excelentes",
            "éxito", "exitoso", "exitosa", "favorables",
            "celebran", "crecimiento", "optimiza", "fortalece",
            "avance", "avances", "innovador", "innovadora",
            "alentadores", "reconocimiento", "apoyo", "eficiencia"
        }

        self.negativas = {
            "negativo", "negativos", "negativa", "negativas",
            "crítica", "críticas", "critican", "preocupación",
            "preocupa", "preocupante", "riesgo", "riesgos",
            "falla", "fallas", "fracasa", "fracaso",
            "error", "errores", "retraso", "retrasos",
            "mala", "mal", "deficiencias", "crisis",
            "pérdidas", "caída", "caídas", "afecta",
            "problemas", "inestable", "abusivas"
        }

    def normalizar(self, texto):
        texto = texto.lower()
        texto = re.sub(r"[^\w\sáéíóúñü]", " ", texto)
        return texto.split()

    def analizar(self, texto):
        tokens = self.normalizar(texto)

        pos = sum(1 for t in tokens if t in self.positivas)
        neg = sum(1 for t in tokens if t in self.negativas)

        total = max(len(tokens), 1)
        score = (pos - neg) / total

        if pos > neg:
            etiqueta = "positivo"
        elif neg > pos:
            etiqueta = "negativo"
        else:
            etiqueta = "neutral"

        return {
            "positivo": pos,
            "negativo": neg,
            "neutral": max(total - pos - neg, 0),
            "compound": score,
            "etiqueta": etiqueta
        }

    def analizar_noticias(self, noticias):
        analizadas = []

        for noticia in noticias:
            texto = f"{noticia['titulo']} {noticia['cuerpo']}"
            sentimiento = self.analizar(texto)

            noticia_analizada = noticia.copy()
            noticia_analizada["sentimiento"] = sentimiento

            analizadas.append(noticia_analizada)

        distribucion = Counter(
            n["sentimiento"]["etiqueta"]
            for n in analizadas
        )

        promedio = sum(
            n["sentimiento"]["compound"]
            for n in analizadas
        ) / max(len(analizadas), 1)

        reporte = {
            "total_analizadas": len(analizadas),
            "distribucion_sentimiento": dict(distribucion),
            "sentimiento_promedio": promedio,
            "tono_general": (
                "positivo" if promedio > 0
                else "negativo" if promedio < 0
                else "neutral"
            )
        }

        return analizadas, reporte