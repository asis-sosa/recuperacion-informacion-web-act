from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import bigrams, trigrams
from collections import Counter
import re
import nltk

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

class AnalisisDiscurso:
    """
    AC-2: Análisis estadístico profundo de textos.
    El alumno lo aplica a textos reales (discursos, artículos, etc.)
    """

    def __init__(self, idioma='spanish'):
        self.stop_words = set(stopwords.words(idioma))
        self.idioma = idioma

    def analizar(self, texto, titulo="Documento"):
        """Análisis completo de un texto."""
        oraciones = sent_tokenize(texto, language=self.idioma)
        tokens = word_tokenize(texto.lower(), language=self.idioma)
        tokens_alfa = [t for t in tokens if t.isalpha() and len(t) > 2]
        tokens_filtrados = [t for t in tokens_alfa if t not in self.stop_words]

        # N-gramas
        bigs = list(bigrams(tokens_filtrados))
        trigs = list(trigrams(tokens_filtrados))

        # Riqueza léxica por secciones (dividir en cuartos)
        cuarto = len(tokens_filtrados) // 4
        riqueza_secciones = []
        for i in range(4):
            seccion = tokens_filtrados[i*cuarto:(i+1)*cuarto]
            if seccion:
                rl = len(set(seccion)) / len(seccion)
                riqueza_secciones.append(rl)

        # Entidades (heurística simple: palabras que inician con mayúscula)
        tokens_original = word_tokenize(texto, language=self.idioma)
        posibles_entidades = [t for t in tokens_original
                            if t[0].isupper() and t.isalpha() and len(t) > 2
                            and t.lower() not in self.stop_words]

        return {
            'titulo': titulo,
            'oraciones': len(oraciones),
            'palabras_totales': len(tokens_alfa),
            'vocabulario_unico': len(set(tokens_filtrados)),
            'riqueza_lexica_global': len(set(tokens_filtrados)) / max(len(tokens_filtrados), 1),
            'riqueza_por_seccion': riqueza_secciones,
            'promedio_palabras_oracion': len(tokens_alfa) / max(len(oraciones), 1),
            'top_unigramas': Counter(tokens_filtrados).most_common(10),
            'top_bigramas': Counter(bigs).most_common(7),
            'top_trigramas': Counter(trigs).most_common(5),
            'posibles_entidades': Counter(posibles_entidades).most_common(8),
        }

    def comparar_textos(self, analisis_lista):
        """Compara estadísticas entre múltiples textos."""
        comparativa = []
        for a in analisis_lista:
            comparativa.append({
                'titulo': a['titulo'],
                'palabras': a['palabras_totales'],
                'vocabulario': a['vocabulario_unico'],
                'riqueza': a['riqueza_lexica_global'],
                'promedio_oracion': a['promedio_palabras_oracion']
            })
        return comparativa


analizador_disc = AnalisisDiscurso()

texto_discurso = """La educación es la herramienta más poderosa para transformar
una sociedad. En México, la inversión en educación debe ser prioritaria para
garantizar el desarrollo económico y social. Los jóvenes mexicanos merecen
oportunidades de calidad en todos los niveles educativos. Las universidades
tecnológicas y los institutos de investigación son pilares fundamentales para
la innovación. La ciencia y la tecnología son motores del progreso nacional.
El Instituto Tecnológico de Morelia ha formado generaciones de ingenieros que
contribuyen al desarrollo del país. La inteligencia artificial y la programación
son competencias esenciales para el futuro laboral. México necesita más
profesionales en ciencias computacionales y recuperación de información."""

texto_cientifico = """El procesamiento de lenguaje natural permite a las computadoras
comprender y generar texto humano. Los modelos de aprendizaje profundo como BERT
y GPT han revolucionado este campo. La representación vectorial de documentos
mediante TF-IDF sigue siendo fundamental para sistemas de recuperación de información.
Los algoritmos de clasificación como Naive Bayes y SVM logran alta precisión en
categorización de texto. El análisis de sentimientos combina técnicas léxicas con
aprendizaje automático para determinar la polaridad emocional de un texto."""

print("=== AC-2: Análisis Estadístico de Discursos ===\n")

analisis1 = analizador_disc.analizar(texto_discurso, "Discurso Educativo")
analisis2 = analizador_disc.analizar(texto_cientifico, "Texto Científico")

for analisis in [analisis1, analisis2]:
    print(f"--- {analisis['titulo']} ---")
    print(f"  Oraciones: {analisis['oraciones']}")
    print(f"  Palabras: {analisis['palabras_totales']}")
    print(f"  Vocabulario: {analisis['vocabulario_unico']}")
    print(f"  Riqueza léxica: {analisis['riqueza_lexica_global']:.3f}")
    print(f"  Prom. palabras/oración: {analisis['promedio_palabras_oracion']:.1f}")
    print(f"  Riqueza por sección: {[f'{r:.3f}' for r in analisis['riqueza_por_seccion']]}")
    print(f"  Top bigramas: {analisis['top_bigramas'][:4]}")
    print(f"  Posibles entidades: {[e[0] for e in analisis['posibles_entidades'][:5]]}")
    print()

print("--- Comparativa ---")
comp = analizador_disc.comparar_textos([analisis1, analisis2])
print(f"{'Texto':<20} {'Palabras':>9} {'Vocab':>7} {'Riqueza':>8} {'P/Oración':>10}")
for c in comp:
    print(f"{c['titulo']:<20} {c['palabras']:>9} {c['vocabulario']:>7} {c['riqueza']:>8.3f} {c['promedio_oracion']:>10.1f}")