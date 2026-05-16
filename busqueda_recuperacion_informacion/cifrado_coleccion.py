from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Base de documentos

documentos_mision3 = [
    {"doc_id": "x1", "nivel": "PUBLICO", "texto": "Boletín de prensa sobre obras en la avenida central y tráfico lento."},

    {"doc_id": "x2", "nivel": "SIGILO", "texto": "Rumor operativo: el contacto cambió frecuencia; verificar handoff nocturno. ###FIN###"},

    {"doc_id": "x3", "nivel": "PUBLICO", "texto": "Convocatoria a curso de primeros auxilios para voluntarios municipales."},

    {"doc_id": "x4", "nivel": "SIGILO", "texto": "Inventario de papelería y tóner para el almacén B del cuartel general."},

    {"doc_id": "x5", "nivel": "RESERVADO", "texto": "Lista de proveedores homologados para catering y cafetería interna."},
]

# Consulta
consulta_mision3 = "contacto frecuencia operativo handoff nocturno"

# 1. Filtrar documentos nivel SIGILO

documentos_sigilo = []

for doc in documentos_mision3:
    if doc["nivel"] == "SIGILO":
        documentos_sigilo.append(doc)

# 2. Extraer IDs y textos

doc_ids = []
textos = []

for doc in documentos_sigilo:
    doc_ids.append(doc["doc_id"])
    textos.append(doc["texto"])

# Agregar consulta al final
todos_los_textos = textos + [consulta_mision3]

# 3. Vectorización TF-IDF

vectorizador = TfidfVectorizer()

matriz_tfidf = vectorizador.fit_transform(todos_los_textos)

# 4. Separar documentos y consulta

matriz_documentos = matriz_tfidf[:-1]

vector_consulta = matriz_tfidf[-1]

# 5. Calcular similitud coseno

similitudes = cosine_similarity(vector_consulta, matriz_documentos)

# Convertir a arreglo simple
similitudes = similitudes.flatten()

# 6. Crear ranking

ranking = []

for i in range(len(doc_ids)):
    ranking.append((doc_ids[i], similitudes[i], textos[i]))

# Ordenar por similitud descendente
ranking.sort(key=lambda x: x[1], reverse=True)

# 7. Obtener mejor documento

mejor_doc = ranking[0]

doc_id_ganador = mejor_doc[0]
puntuacion = mejor_doc[1]
texto_ganador = mejor_doc[2]

# Recorte de 120 caracteres
fragmento = texto_ganador[:120]

# 8. Mostrar resultado

print("DOCUMENTO MÁS RELEVANTE:\n")

print(f"doc_id: {doc_id_ganador}")
print(f"similitud: {puntuacion:.4f}")

print("\nFragmento:")
print(fragmento)