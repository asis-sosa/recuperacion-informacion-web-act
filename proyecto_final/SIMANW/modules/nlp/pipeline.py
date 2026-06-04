import re
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


class PipelineNLP:
    def __init__(self, idioma="spanish"):
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        nltk.download("stopwords", quiet=True)

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

    def procesar_texto(self, texto):
        limpio = self.limpiar(texto)
        tokens = self.tokenizar(limpio)
        sin_stopwords = self.eliminar_stopwords(tokens)
        stems = self.aplicar_stemming(sin_stopwords)

        return {
            "limpio": limpio,
            "tokens": tokens,
            "sin_stopwords": sin_stopwords,
            "stems": stems,
            "num_oraciones": len(sent_tokenize(texto, language=self.idioma)),
            "vocabulario_unico": len(set(sin_stopwords)),
            "riqueza_lexica": len(set(sin_stopwords)) / max(len(sin_stopwords), 1)
        }

    def procesar_noticias(self, noticias):
        procesadas = []

        for noticia in noticias:
            texto = f"{noticia['titulo']}. {noticia['cuerpo']}"
            resultado = self.procesar_texto(texto)

            noticia_procesada = noticia.copy()
            noticia_procesada["nlp"] = resultado

            procesadas.append(noticia_procesada)

        return procesadas

    def estadisticas_corpus(self, noticias_procesadas):
        todos_tokens = []
        todos_stems = []

        for noticia in noticias_procesadas:
            todos_tokens.extend(noticia["nlp"]["sin_stopwords"])
            todos_stems.extend(noticia["nlp"]["stems"])

        return {
            "total_documentos": len(noticias_procesadas),
            "total_tokens": len(todos_tokens),
            "vocabulario_total": len(set(todos_tokens)),
            "stems_unicos": len(set(todos_stems)),
            "palabras_frecuentes": Counter(todos_tokens).most_common(10),
            "promedio_tokens_doc": len(todos_tokens) / max(len(noticias_procesadas), 1)
        }