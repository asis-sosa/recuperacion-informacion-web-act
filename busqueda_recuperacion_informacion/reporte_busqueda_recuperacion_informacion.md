#  Reporte de Misión: Búsqueda y Recuperación de Información
**Agente Especial:** Sebastian Asis Sosa Santiag / 22120720

---
## Misión 1, 2 y 3
[Incluir aquí los bloques de código Python y las salidas (rankings, doc_id, etc.)]

### Misión 1

```python
corpus_mision1 = {
    "d1": "La red de agentes interceptó tráfico sospechoso en el nodo norte.",
    "d2": "El agente de campo reportó actividad normal en la red interna.",
    "d3": "Manual de procedimientos: la red no debe apagarse sin autorización.",
    "d4": "Mantenimiento programado del agente automático de respaldo.",
}

# 1. Tokenización y creación del índice invertido

indice_invertido = {}

# Recorrer cada documento del corpus
for doc_id, texto in corpus_mision1.items():

    texto = texto.lower()

    texto = texto.replace(".", "")
    texto = texto.replace(",", "")
    texto = texto.replace(":", "")

    # Tokenizar
    tokens = texto.split()

    for token in tokens:
        # Si el término no existe en el índice, crearlo
        if token not in indice_invertido:
            indice_invertido[token] = []

        # Evitar documentos repetidos
        if doc_id not in indice_invertido[token]:
            indice_invertido[token].append(doc_id)

print("ÍNDICE INVERTIDO:\n")

for termino, documentos in sorted(indice_invertido.items()):
    print(f"{termino} -> {documentos}")

# 2. Consulta booleana: "agente" AND "red"

termino1 = "agente"
termino2 = "red"

# Obtener listas de documentos
docs_termino1 = set(indice_invertido.get(termino1, []))
docs_termino2 = set(indice_invertido.get(termino2, []))

# Operación AND (intersección)
resultado = sorted(docs_termino1.intersection(docs_termino2))

# 3. Mostrar resultados

print("\nRESULTADO DE LA CONSULTA:")
print(f'"{termino1}" AND "{termino2}"')

print("\nDocumentos coincidentes:")
print(resultado)
```

### Salida Misión 1

ÍNDICE INVERTIDO:

- actividad -> ['d2']
- agente -> ['d2', 'd4']
- agentes -> ['d1']
- apagarse -> ['d3']
- automático -> ['d4']
- autorización -> ['d3']
- campo -> ['d2']
- de -> ['d1', 'd2', 'd3', 'd4']
- debe -> ['d3']
- del -> ['d4']
- el -> ['d1', 'd2']
- en -> ['d1', 'd2']
- interceptó -> ['d1']
- interna -> ['d2']

### Misión 2

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

corpus_mision2 = {
    "a1": "Protocolo de evacuación silenciosa en instalaciones subterráneas.",
    "a2": "Guía de rutas de escape y puntos de reunión sin alarmas audibles.",
    "a3": "Receta de cocina: pasta con tomate y albahaca para el personal.",
    "a4": "Mapa de salidas de emergencia y señalética fotoluminiscente.",
    "a5": "Informe meteorológico: probabilidad de lluvia en la región este.",
}

consulta_mision2 = "evacuación silenciosa rutas de escape emergencia"

# 1. Preparar documentos
doc_ids = list(corpus_mision2.keys())
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

print("TOP 3 DOCUMENTOS MÁS RELEVANTES:\n")

for doc_id, puntuacion in ranking[:3]:
    print(f"{doc_id}: {puntuacion:.4f}")
```

### Salida Misión 2

TOP 3 DOCUMENTOS MÁS RELEVANTES:
- a1: 0.3579
- a2: 0.3398
- a4: 0.2419

### Misión 3

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documentos_mision3 = [
    {"doc_id": "x1", "nivel": "PUBLICO", "texto": "Boletín de prensa sobre obras en la avenida central y tráfico lento."},

    {"doc_id": "x2", "nivel": "SIGILO", "texto": "Rumor operativo: el contacto cambió frecuencia; verificar handoff nocturno. ###FIN###"},

    {"doc_id": "x3", "nivel": "PUBLICO", "texto": "Convocatoria a curso de primeros auxilios para voluntarios municipales."},

    {"doc_id": "x4", "nivel": "SIGILO", "texto": "Inventario de papelería y tóner para el almacén B del cuartel general."},

    {"doc_id": "x5", "nivel": "RESERVADO", "texto": "Lista de proveedores homologados para catering y cafetería interna."},
]

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

print("DOCUMENTO MÁS RELEVANTE:\n")

print(f"doc_id: {doc_id_ganador}")
print(f"similitud: {puntuacion:.4f}")

print("\nFragmento:")
print(fragmento)
```

### Salida Misión 3

DOCUMENTO MÁS RELEVANTE:

- doc_id: x2
- similitud: 0.6222
- Fragmento: Rumor operativo, el contacto cambió frecuencia; verificar handoff nocturno. ###FIN###

---
##  Análisis del Analista (Reflexiones Finales)

1. **Sobre la Investigación (Misión 1):** Explica con tus propias palabras qué es un índice invertido y por qué la intersección de postings implementa un AND booleano en este modelo.
> Un indice invertido es practicamente un indice que relaciona terminos con contenido, pero en vez de tener los terminos o en este caso documentos, se tiene los contenidos o en este caso las palabras mas importantes de ese contenido y se relacionan con los terminos en base a su presencia, se podria decir que si se buscase cierta frase y se tomara las palabras mas importantes, en vez de ir buscando de documento en documento, solamente seria utilizar encontrar una coincidencia de palabras importantes y encontrar los documentos en donde aparecen y es aqui donde se hace presencia el metodo "AND booleano" que practicamente se aprovecha del sistema "AND", donde ambos deben estar presentes para dar un afirmativo, contar con diferentes palabras y utilizarlo, facilita la busqueda y extraccion de los documentos que tengan relacion con la frase buscada.

2. **Sobre TF-IDF (Misión 2):** ¿Por qué un término muy frecuente en *todos* los documentos suele discriminar peor que un término raro pero presente en pocos? Relacióna tu explicación con *idf*.
> La presencia de un termino comun para la busqueda de informacion donde la coincidencia de terminos es clave es totalmente inpensable, no tendria sentido tener todos los terminos para encontrar una sola informacion, el uso de terminos pocos frecuentes, importantes, proporciona un enfoque mas preciso a la busqueda, esto se relaciona con idf porque este relaciona importancia con frecuencia, donde un termino que apazca en multiples documentos cuenta con un idf bajo, caso contrario con uno que aparece en pocos documentos teniendo un idf alto.

3. **Sobre la Lógica de Recuperación (Misión 3):** Si aplicaras TF-IDF a *toda* la colección (sin filtrar por =SIGILO=), ¿cómo podría cambiar el documento top-1 y por qué el filtro actúa como una *llave de acceso* antes del ranking?
> Funciona como una llave de acceso, ya que es un modo de seguridad que permite filtrar todos los documentos, hacia los que en verdad nos interesan, si no se utilizara todos los documentos serian importantes en la busqueda y todo el filtrado de TF-IDF y similitud coseno actuarian en todos ellos, cambian por completo el resultado hacia alguno que mas se relacione con la consulta.