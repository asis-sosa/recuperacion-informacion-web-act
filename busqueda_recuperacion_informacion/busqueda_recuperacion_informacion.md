# Expediente X: Búsqueda y Recuperación de la Información

## Introduación para los Agentes

La búsqueda en colecciones de texto no siempre es un cuadro de texto y un botón. Detrás hay modelos de coincidencia, índices, ponderación de términos y, a veces, filtros que actúan como llaves antes de rankear resultados. Su misión de hoy consta de tres fases para localizar fragmentos clasificados dentro de un corpus interceptado (documentos de ejemplo que ustedes mismos construirán o cargarán desde variables en código).

## Misión 1: La Telaraña de Tokens (Investigación e Índice Invertido Básico)

La Historia: Hemos interceptado una serie de informes en texto plano (corpus_mision1). Los archivos no están cifrados, pero están desordenados conceptualmente: necesitamos saber en qué documentos aparece cada palabra para poder responder consultas tipo biblioteca clásica.

Tu Tarea:

- Fase de Investigación: Antes de programar, investiga en internet:
  - ¿Qué es un índice invertido (inverted index)?

La indexación invertida es un método de indexación que se utiliza para almacenar el mapeo de la ubicación de almacenamiento de una palabra en un documento o un grupo de documentos en búsqueda de texto completo.

Tomando el inglés como ejemplo, aquí está el texto a indexar:

```python
T0 = "it is what it is"  
T1 = "what is it"  
T2 = "it is a banana"  
```

Podemos obtener el siguiente índice de archivo inverso:

```python
"a":      {2}
"banana": {2}
"is":     {0, 1, 2}
"it":     {0, 1, 2}
"what":   {0, 1} 
```

Las condiciones de búsqueda "what", "is" y "it" corresponderán a la intersección de conjuntos.

El índice de avance se desarrolló para almacenar una lista de palabras para cada documento. La consulta indexada directa a menudo satisface el orden de consultas frecuentes de texto completo de cada documento y la verificación de cada palabra en el documento de verificación. En un índice hacia adelante, los documentos ocupan la posición central, y cada documento apunta a una secuencia de elementos de índice que contiene. En otras palabras, el documento apunta a las palabras que contiene, y el índice inverso se refiere a las palabras que apuntan al documento que lo contiene. Es fácil ver la relación inversa.

  - ¿Qué relación tiene con la tokenización y la lista de postings?

La tokenización es el proceso de dividir un documento en unidades más pequeñas llamadas tokens. Cada token usualmente representa una palabra, número o símbolo significativo. Este proceso es crucial porque transforma un texto libre en elementos que pueden ser indexados.

Una lista de postings (o posting list) es una estructura que almacena información sobre en qué documentos aparece cada token en el índice invertido. Cada token generado durante la tokenización servirá como una clave en el índice, y su lista de postings contendrá los identificadores de documentos y, opcionalmente, posiciones, frecuencias o pesos.

1. **Generación de clave para el índice:** Cada token producido en la tokenización se convierte en una entrada en el índice invertido. Sin tokenización, no sería posible identificar las unidades mínimas de búsqueda.
2. **Población de postings:** Una vez que se identifican los tokens en los documentos, se actualizan las listas de postings para registrar en qué documentos aparece cada token.
3. **Precisión en la búsqueda:** Tokenización eficiente (considerando sinónimos, normalización de caracteres, eliminación de stopwords, etc.) mejora la exactitud de las listas de postings y, por ende, la relevancia de los resultados de búsqueda.
4. **Optimización de espacio y velocidad:** Al tokenizar correctamente, las listas de postings son más coherentes y compactas, lo que permite búsquedas rápidas y eficientes en grandes volúmenes de texto.

- Fase de Construcción: Construye en Python un índice invertido case-insensitive (minúsculas) a partir del diccionario de documentos siguiente (cada clave es un doc_id, cada valor es el texto). Debes:
  - Tokenizar (puedes usar solo split() y limpieza básica de puntuación simple).
  - Para la consulta booleana agente AND red, devolver la intersección de listas de postings (documentos que contienen ambas palabras).
  - Imprimir los doc_id resultantes ordenados alfabéticamente.

```python
corpus_mision1 = {
    "d1": "La red de agentes interceptó tráfico sospechoso en el nodo norte.",
    "d2": "El agente de campo reportó actividad normal en la red interna.",
    "d3": "Manual de procedimientos: la red no debe apagarse sin autorización.",
    "d4": "Mantenimiento programado del agente automático de respaldo.",
}

# ESCRIBE TU CÓDIGO AQUÍ:
# 1) Tokenizar y construir índice invertido: término -> lista de doc_id
# 2) Resolver la consulta booleana: "agente" AND "red"
# 3) Imprimir doc_id coincidentes, ordenados
```
## Misión 2: Operación Vector de Consulta (Recuperación por TF-IDF)

La Historia: El enemigo dejó de organizar la información solo con palabras sueltas. Ahora los informes son casi sinónimos entre sí: la coincidencia literal (AND) falla. Interceptamos un corpus_mision2 más grande; debemos rankear documentos por similitud vectorial frente a una consulta en lenguaje natural.

- Las Pistas:
  - Puedes usar sklearn.feature_extraction.text.TfidfVectorizer y sklearn.metrics.pairwise.cosine_similarity.
  - Si no tienes instalada la librería: pip install scikit-learn.
- Tu Tarea
  - Representa los documentos y la consulta en el espacio TF-IDF.
  - Calcula la similitud coseno entre la consulta y cada documento.
  - Imprime un ranking (de mayor a menor similitud) con formato: doc_id: puntuación para los tres documentos más relevantes.

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

# ESCRIBE TU CÓDIGO AQUÍ:
# 1) Vectorizar corpus + consulta (mismo vectorizador)
# 2) cosine_similarity entre vector de consulta y matriz de documentos
# 3) Imprimir top-3 doc_id con puntuación
```

## Misión 3: El Cifrado de Colección (Reto Híbrido: Filtro + TF-IDF)

La Historia: ¡El reto final! El enemigo duplicó vocabulario en toda la base: hay ruido semántico global. Los fragmentos realmente clasificados están marcados con una llave de metadatos: solo los documentos con nivel"SIGILO"= contienen, concatenados en el orden del ranking, pistas que terminan con el delimitador ###FIN### en el texto original (simulado aquí como un solo documento “jefe” que debes encontrar).

- Las Pistas:
  - Llave de colección: procesar únicamente los documentos cuyo campo nivel sea SIGILO.
  - Luego aplica TF-IDF solo sobre ese subconjunto y rankea frente a la consulta dada.
  - El mensaje recuperado es el texto completo del documento rankeado en primer lugar (debe contener ###FIN### al final en la plantilla de datos; si generas tus propios textos, respeta ese delimitador en el doc top-1).
- Tu Tarea
  - Filtra la lista de documentos por nivel = "SIGILO"=.
  - Construye TF-IDF y rankea con similitud coseno frente a la consulta.
  - Imprime el doc_id ganador y las primeras 120 caracteres de su texto (suficiente para ver contexto y el delimitador si está al final).

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

# ESCRIBE TU CÓDIGO AQUÍ:
# 1) Filtrar nivel SIGILO
# 2) TF-IDF + cosine similarity vs consulta
# 3) Imprimir doc_id top-1 y recorte de 120 caracteres del texto
```

## Entregable: Reporte de Misión (Formato Markdown)

Deben entregar un archivo reporte_mision_busqueda.md con la siguiente estructura. Deberán incluir sus códigos, salidas (texto) de cada misión en consola, y responder a las preguntas del Análisis del Analista.

```markdown
#  Reporte de Misión: Búsqueda y Recuperación de Información
**Agente Especial:** [Tu Nombre/Matrícula]

---
## Misión 1, 2 y 3
[Incluir aquí los bloques de código Python y las salidas (rankings, doc_id, etc.)]

---
##  Análisis del Analista (Reflexiones Finales)

1. **Sobre la Investigación (Misión 1):** Explica con tus propias palabras qué es un índice invertido y por qué la intersección de postings implementa un AND booleano en este modelo.
> *[Tu respuesta]*

2. **Sobre TF-IDF (Misión 2):** ¿Por qué un término muy frecuente en *todos* los documentos suele discriminar peor que un término raro pero presente en pocos? Relacióna tu explicación con *idf*.
> *[Tu respuesta]*

3. **Sobre la Lógica de Recuperación (Misión 3):** Si aplicaras TF-IDF a *toda* la colección (sin filtrar por =SIGILO=), ¿cómo podría cambiar el documento top-1 y por qué el filtro actúa como una *llave de acceso* antes del ranking?
> *[Tu respuesta]*
```