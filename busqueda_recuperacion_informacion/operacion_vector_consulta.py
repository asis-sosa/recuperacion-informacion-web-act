from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Corpus de documentos

corpus_mision2 = {
    "a1": "Protocolo de evacuación silenciosa en instalaciones subterráneas.",
    "a2": "Guía de rutas de escape y puntos de reunión sin alarmas audibles.",
    "a3": "Receta de cocina: pasta con tomate y albahaca para el personal.",
    "a4": "Mapa de salidas de emergencia y señalética fotoluminiscente.",
    "a5": "Informe meteorológico: probabilidad de lluvia en la región este.",
}

# Consulta
consulta_mision2 = "evacuación silenciosa rutas de escape emergencia"

# 1. Preparar documentos

# Obtener IDs de documentos
doc_ids = list(corpus_mision2.keys())

# Obtener textos de documentos
documentos = list(corpus_mision2.values())

# Agregar consulta al final
todos_los_textos = documentos + [consulta_mision2]

# 2. Vectorización TF-IDF

vectorizador = TfidfVectorizer()

# Crear matriz TF-IDF
matriz_tfidf = vectorizador.fit_transform(todos_los_textos)

# 3. Separar documentos y consulta

# Matriz de documentos
matriz_documentos = matriz_tfidf[:-1]

# Vector de la consulta
vector_consulta = matriz_tfidf[-1]

# 4. Calcular similitud coseno

similitudes = cosine_similarity(vector_consulta, matriz_documentos)

# Convertir a lista simple
similitudes = similitudes.flatten()

# 5. Crear ranking

ranking = []

for i in range(len(doc_ids)):
    ranking.append((doc_ids[i], similitudes[i]))

# Ordenar de mayor a menor similitud
ranking.sort(key=lambda x: x[1], reverse=True)

# 6. Mostrar Top-3

print("TOP 3 DOCUMENTOS MÁS RELEVANTES:\n")

for doc_id, puntuacion in ranking[:3]:
    print(f"{doc_id}: {puntuacion:.4f}")