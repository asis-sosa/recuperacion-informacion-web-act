import nltk
import re
from collections import Counter

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "categoria_original": "tecnologia"
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas.",
        "categoria_original": "economia"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio sobre el calentamiento global.",
        "categoria_original": "ciencia"
    }
]


class PipelineNLP:
    def __init__(self, idioma="spanish"):
        self.idioma = idioma
        self.stemmer = SnowballStemmer(idioma)
        self.stop_words = set(stopwords.words(idioma))

    def limpiar(self, texto):
        texto = texto.lower()
        texto = re.sub(r"[^\w\sáéíóúñü]", " ", texto)
        texto = re.sub(r"\d+", "", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto

    def tokenizar(self, texto):
        return word_tokenize(texto, language=self.idioma)

    def eliminar_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stop_words and len(t) > 2]

    def aplicar_stemming(self, tokens):
        return [self.stemmer.stem(t) for t in tokens]

    def procesar(self, texto):
        limpio = self.limpiar(texto)
        tokens = self.tokenizar(limpio)
        sin_sw = self.eliminar_stopwords(tokens)
        stems = self.aplicar_stemming(sin_sw)

        return {
            "original": texto,
            "limpio": limpio,
            "tokens": tokens,
            "sin_stopwords": sin_sw,
            "stems": stems,
            "num_oraciones": len(sent_tokenize(texto, language=self.idioma)),
            "vocabulario_unico": len(set(sin_sw)),
            "riqueza_lexica": len(set(sin_sw)) / max(len(sin_sw), 1),
        }

    def estadisticas_corpus(self, textos_procesados):
        todos_tokens = []
        todos_stems = []

        for tp in textos_procesados:
            todos_tokens.extend(tp["sin_stopwords"])
            todos_stems.extend(tp["stems"])

        return {
            "total_documentos": len(textos_procesados),
            "total_tokens": len(todos_tokens),
            "vocabulario_total": len(set(todos_tokens)),
            "stems_unicos": len(set(todos_stems)),
            "palabras_frecuentes": Counter(todos_tokens).most_common(10),
            "promedio_tokens_doc": len(todos_tokens) / max(len(textos_procesados), 1),
        }


pipeline = PipelineNLP()

print("=== FASE 2.1: Pipeline NLP ===\n")
print("Procesando noticias extraídas...\n")

noticias_procesadas = []

for noticia in noticias:
    texto_completo = f"{noticia['titulo']}. {noticia['cuerpo']}"

    resultado = pipeline.procesar(texto_completo)
    noticia["nlp"] = resultado
    noticias_procesadas.append(resultado)

    print(f"[{noticia['categoria_original']}] {noticia['titulo'][:50]}...")
    print(f"  Tokens: {len(resultado['tokens'])}")
    print(f"  Sin stopwords: {len(resultado['sin_stopwords'])}")
    print(f"  Stems: {len(resultado['stems'])}")
    print(f"  Riqueza léxica: {resultado['riqueza_lexica']:.3f}")
    print(f"  Tokens limpios: {resultado['sin_stopwords']}")
    print(f"  Stems: {resultado['stems']}")
    print()

stats = pipeline.estadisticas_corpus(noticias_procesadas)

print("--- Estadísticas del Corpus ---")
for k, v in stats.items():
    if k != "palabras_frecuentes":
        print(f"{k}: {v}")

print("\nPalabras más frecuentes:")
for palabra, freq in stats["palabras_frecuentes"]:
    print(f"'{palabra}': {freq}")