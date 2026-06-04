from collections import Counter, defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MotorBusqueda:
    def __init__(self):
        self.documentos = {}
        self.indice_invertido = defaultdict(dict)
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.matriz_busqueda = None

    def indexar(self, documentos):
        textos = []

        for doc_id, doc in enumerate(documentos):
            self.documentos[doc_id] = doc
            texto = f"{doc['titulo']} {doc['cuerpo']}"
            textos.append(texto)

            tokens = texto.lower().split()
            frecuencias = Counter(tokens)

            for termino, freq in frecuencias.items():
                self.indice_invertido[termino][doc_id] = freq

        self.matriz_busqueda = self.vectorizer.fit_transform(textos)

    def buscar_booleana(self, consulta, modo="AND"):
        terminos = consulta.lower().split()

        if not terminos:
            return []

        if modo == "AND":
            resultado = set(self.indice_invertido.get(terminos[0], {}).keys())

            for termino in terminos[1:]:
                resultado &= set(self.indice_invertido.get(termino, {}).keys())

        else:
            resultado = set()

            for termino in terminos:
                resultado |= set(self.indice_invertido.get(termino, {}).keys())

        return list(resultado)

    def buscar_vectorial(self, consulta, top_k=5):
        if self.matriz_busqueda is None:
            return []

        consulta_vec = self.vectorizer.transform([consulta])
        similitudes = cosine_similarity(consulta_vec, self.matriz_busqueda)[0]
        indices = similitudes.argsort()[::-1][:top_k]

        resultados = []

        for idx in indices:
            if similitudes[idx] > 0:
                doc = self.documentos[idx]

                resultados.append({
                    "doc_id": idx,
                    "titulo": doc["titulo"],
                    "relevancia": float(similitudes[idx]),
                    "categoria": doc.get("categoria_predicha", doc.get("categoria_original", "?")),
                    "sentimiento": doc.get("sentimiento", {}).get("etiqueta", "?"),
                    "snippet": doc["cuerpo"][:120] + "...",
                    "url": doc.get("url", "")
                })

        return resultados

    def info_indice(self):
        return {
            "documentos_indexados": len(self.documentos),
            "terminos_en_indice": len(self.indice_invertido),
            "features_vectoriales": self.matriz_busqueda.shape[1] if self.matriz_busqueda is not None else 0
        }