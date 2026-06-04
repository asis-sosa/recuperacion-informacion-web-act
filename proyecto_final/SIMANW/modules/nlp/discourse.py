from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import bigrams, trigrams
from collections import Counter
import nltk

class AnalisisDiscurso:
    def __init__(self, idioma="spanish"):
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        nltk.download("stopwords", quiet=True)
        self.stop_words = set(stopwords.words(idioma))
        self.idioma = idioma

    def analizar(self, texto, titulo="Corpus SIMANW"):
        oraciones = sent_tokenize(texto, language=self.idioma)
        tokens = word_tokenize(texto.lower(), language=self.idioma)
        tokens_alfa = [t for t in tokens if t.isalpha() and len(t) > 2]
        tokens_filtrados = [t for t in tokens_alfa if t not in self.stop_words]

        bigs = list(bigrams(tokens_filtrados))
        trigs = list(trigrams(tokens_filtrados))

        cuarto = max(len(tokens_filtrados) // 4, 1)
        riqueza_secciones = []

        for i in range(4):
            seccion = tokens_filtrados[i * cuarto:(i + 1) * cuarto]
            if seccion:
                riqueza_secciones.append(len(set(seccion)) / len(seccion))

        tokens_original = word_tokenize(texto, language=self.idioma)
        posibles_entidades = [
            t for t in tokens_original
            if t[:1].isupper()
            and t.isalpha()
            and len(t) > 2
            and t.lower() not in self.stop_words
        ]

        return {
            "titulo": titulo,
            "oraciones": len(oraciones),
            "palabras_totales": len(tokens_alfa),
            "vocabulario_unico": len(set(tokens_filtrados)),
            "riqueza_lexica_global": len(set(tokens_filtrados)) / max(len(tokens_filtrados), 1),
            "riqueza_por_seccion": riqueza_secciones,
            "promedio_palabras_oracion": len(tokens_alfa) / max(len(oraciones), 1),
            "top_unigramas": Counter(tokens_filtrados).most_common(10),
            "top_bigramas": Counter(bigs).most_common(7),
            "top_trigramas": Counter(trigs).most_common(5),
            "posibles_entidades": Counter(posibles_entidades).most_common(8),
        }