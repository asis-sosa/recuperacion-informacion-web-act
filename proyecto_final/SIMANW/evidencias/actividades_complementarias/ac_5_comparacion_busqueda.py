from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa transforman múltiples industrias."
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación."
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio sobre calentamiento global y emisiones."
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión de Python mejora el desarrollo y la programación."
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma ofrece datasets públicos en RDF y JSON-LD para datos abiertos."
    }
]

class ComparadorModelos:
    """
    AC-5: Compara formalmente modelo booleano vs. vectorial.
    El alumno documenta qué modelo funciona mejor y por qué.
    """

    def __init__(self, documentos):
        self.documentos = documentos
        self.textos = [f"{d['titulo']} {d['cuerpo']}" for d in documentos]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matriz = self.vectorizer.fit_transform(self.textos)

        # Índice invertido para modelo booleano
        self.indice = {}
        for i, texto in enumerate(self.textos):
            for palabra in texto.lower().split():
                if palabra not in self.indice:
                    self.indice[palabra] = set()
                self.indice[palabra].add(i)

    def busqueda_booleana(self, consulta):
        """Modelo booleano: AND de todos los términos."""
        terminos = consulta.lower().split()
        if not terminos:
            return []
        resultado = self.indice.get(terminos[0], set()).copy()
        for t in terminos[1:]:
            resultado &= self.indice.get(t, set())
        return sorted(resultado)

    def busqueda_vectorial(self, consulta, top_k=5):
        """Modelo vectorial: ranking por similitud coseno."""
        q_vec = self.vectorizer.transform([consulta])
        sims = cosine_similarity(q_vec, self.matriz)[0]
        indices = sims.argsort()[::-1][:top_k]
        return [(i, sims[i]) for i in indices if sims[i] > 0]

    def evaluar_ambos(self, consulta, relevantes):
        """Evalúa ambos modelos con la misma consulta y juicio de relevancia."""
        # Booleano
        bool_result = self.busqueda_booleana(consulta)
        bool_precision = len(set(bool_result) & set(relevantes)) / max(len(bool_result), 1)
        bool_recall = len(set(bool_result) & set(relevantes)) / max(len(relevantes), 1)

        # Vectorial
        vec_result = [idx for idx, _ in self.busqueda_vectorial(consulta, top_k=len(self.documentos))]
        vec_top_k = vec_result[:len(bool_result)] if bool_result else vec_result[:3]
        vec_precision = len(set(vec_top_k) & set(relevantes)) / max(len(vec_top_k), 1)
        vec_recall = len(set(vec_top_k) & set(relevantes)) / max(len(relevantes), 1)

        return {
            'consulta': consulta,
            'booleano': {
                'recuperados': len(bool_result),
                'precision': bool_precision,
                'recall': bool_recall
            },
            'vectorial': {
                'recuperados': len(vec_top_k),
                'precision': vec_precision,
                'recall': vec_recall
            }
        }


comparador = ComparadorModelos(noticias)

# Consultas de evaluación con juicios de relevancia manuales
consultas_eval = [
    {"consulta": "inteligencia artificial", "relevantes": [0, 3]},
    {"consulta": "mercados volatilidad economía", "relevantes": [1]},
    {"consulta": "datos abiertos gobierno", "relevantes": [4]},
    {"consulta": "cambio climático científico", "relevantes": [2]},
]

print("=== AC-5: Comparación Booleano vs. Vectorial ===\n")
print(f"{'Consulta':<30} | {'Modelo':<10} | {'Recup':>5} | {'Prec':>6} | {'Recall':>6}")
print("─" * 75)

sum_bool_p, sum_vec_p = 0, 0
sum_bool_r, sum_vec_r = 0, 0

for ce in consultas_eval:
    resultado = comparador.evaluar_ambos(ce['consulta'], ce['relevantes'])
    b = resultado['booleano']
    v = resultado['vectorial']
    sum_bool_p += b['precision']
    sum_vec_p += v['precision']
    sum_bool_r += b['recall']
    sum_vec_r += v['recall']
    print(f"{ce['consulta']:<30} | {'Booleano':<10} | {b['recuperados']:>5} | {b['precision']:>6.3f} | {b['recall']:>6.3f}")
    print(f"{'':30} | {'Vectorial':<10} | {v['recuperados']:>5} | {v['precision']:>6.3f} | {v['recall']:>6.3f}")
    print()

n = len(consultas_eval)
print("─" * 75)
print(f"{'PROMEDIO':<30} | {'Booleano':<10} | {'':>5} | {sum_bool_p/n:>6.3f} | {sum_bool_r/n:>6.3f}")
print(f"{'':30} | {'Vectorial':<10} | {'':>5} | {sum_vec_p/n:>6.3f} | {sum_vec_r/n:>6.3f}")
print(f"\nConclusion: El modelo {'vectorial' if sum_vec_p > sum_bool_p else 'booleano'} tiene mejor precision promedio.")