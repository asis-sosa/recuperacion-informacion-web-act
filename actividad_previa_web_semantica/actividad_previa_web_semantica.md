# Actividad previa Web Semántica

## Para el estudiante

Antes de estudiar RDF, OWL y SPARQL (ver web_semantica.org), esta actividad construye la intuición que esos estándares formalizan:

- La Web «normal» mezcla presentación (HTML) y datos (JSON, CSV).
- Una máquina no «entiende» un párrafo; necesita hechos estructurados y identificadores estables.
- Un grafo (nodos + relaciones tipadas) generaliza tablas y enlaces.
- La ambigüedad de nombres («París» ciudad vs. persona) exige URIs y vocabularios compartidos.

## Prerrequisitos sugeridos:

- HTML básico y, si es posible, nociones de JSON.
- Python 3 (solo biblioteca estándar en las misiones 1 y 3; misión 2 opcional sin red).
- Haber leído al menos la introducción de recuperación de información (búsqueda por palabras clave) ayuda a contrastar con consultas sobre grafos.

## Misión 0: Calentamiento (investigación breve, 15 min)

Responde por escrito (medio párrafo cada punto) antes de programar:

1. ¿Qué diferencia hay entre una página web que describe a un museo y un dataset que lista museos con coordenadas y horarios?
2. Busca «*Tim Berners-Lee four rules of linked data*» o «*cinco estrellas datos abiertos*». Resume con tus palabras qué significa que un dato esté «enlazado».
3. Abre en el navegador la consulta de ejemplo de Wikidata Query Service (https://query.wikidata.org/) y ejecuta una consulta de demostración. ¿El resultado parece una tabla SQL o algo distinto? Anota una observación.

### Espacio para tus respuestas (o en tu reporte .md)
1.
2.
3.

## Misión 1: Extracción manual de «triples» desde HTML y JSON

- La historia

Interceptaste un informe en HTML sobre una persona y un archivo JSON con datos de una biblioteca. El buscador por palabras clave encuentra «García» en ambos, pero no sabe si es la misma persona. Tu equipo debe extraer hechos en forma (sujeto, predicado, objeto) como haría RDF antes de tener sintaxis Turtle.

- Datos de entrada (no modificar)

```python
html_informe = """
<article id="persona-alicia">
  <h1>Alicia García</h1>
  <p class="rol">Profesora de Matemáticas en la UNAM</p>
  <p>Conoce a <a href="/personas/bob">Bob Martínez</a>, coautor del artículo
     <cite>Redes y Grafos</cite>.</p>
</article>
"""

json_biblioteca = {
    "libro_id": "L-42",
    "titulo": "Introducción a la Web Semántica",
    "autores": ["Alicia García", "Bob Martínez"],
    "anio": 2019,
    "isbn": "978-3-030-00000-0",
}
```

- Tu tarea
  - Escribe al menos 6 triples en español o en notación (sujeto, predicado, objeto) tomados del HTML (usa identificadores inventados si hace falta, p. ej. ex:alicia).
  - Escribe al menos 4 triples tomados del JSON.
  - Señala un triple que aparece «casi igual» en ambas fuentes pero con sujetos distintos si no unificas identificadores. Explica por qué eso es un problema para una máquina.

```python
# OPCIONAL: validar que tus triples cubren campos clave
triples_html = [
    # ("ex:alicia", "tieneNombre", "Alicia García"),
    # ...
]

triples_json = [
    # ...
]

def cubre(triples, predicados_esperados):
    preds = {p for _, p, _ in triples}
    faltan = set(predicados_esperados) - preds
    print("Predicados presentes:", sorted(preds))
    print("Faltan:", sorted(faltan) if faltan else "ninguno")

cubre(triples_html, {"tieneNombre", "tieneRol", "conoce", "coautorDe"})
cubre(triples_json, {"titulo", "tieneAutor", "publicadoEn"})
```

- Pregunta de cierre (Misión 1)

Si mañana el HTML cambia la etiqueta "h1" a mayúsculas o mueve el nombre a una etiqueta "span", ¿tu extracción manual sigue siendo válida? Relaciona la respuesta con la idea de separar datos y presentación.

## Misión 2: URIs, sinónimos y el problema «París»

- La historia

Tres fuentes usan nombres distintos para la misma entidad y la misma cadena para cosas distintas. Debes diseñar una tabla de identificadores globales (URI ficticia) antes de fusionar grafos.

- Datos

```python
fuente_a = [
    ("París", "esCapitalDe", "Francia"),
    ("París Hilton", "esTipo", "Persona"),
    ("FR", "nombreOficial", "République française"),
]

fuente_b = [
    ("http://geo.example/city/paris", "capital", "http://geo.example/country/fr"),
    ("http://people.example/paris_hilton", "rdf:type", "Person"),
    ("http://geo.example/country/fr", "label", "France"),
]

fuente_c = {
    "wd:Q90": "París (ciudad)",
    "wd:Q47899": "Paris Hilton",
    "wd:Q142": "Francia",
}
```

- Tu tarea (papel o Org, luego opcional en código)
  - Construye una tabla (en tu reporte) con columnas: nombre_en_texto | URI_propuesta | tipo_entidad para cada fila problemática de fuente_a.
  - Propón al menos dos triples de alineación entre fuente_a y fuente_b usando un predicado como owl:sameAs o skos:exactMatch (puedes usar URIs inventadas).
  - Explica en 3–4 líneas por qué la búsqueda literal del término «París» en un motor de keywords no basta y qué aporta un identificador URI.

```python
# OPCIONAL: simular fusión por diccionario URI -> etiqueta legible
uri_labels = {
    "http://geo.example/city/paris": "París (ciudad)",
    "http://people.example/paris_hilton": "Paris Hilton",
    "http://geo.example/country/fr": "Francia",
}

same_as = {
    "París": "http://geo.example/city/paris",
    "Francia": "http://geo.example/country/fr",
}

def resolver(nombre_o_uri):
  return uri_labels.get(nombre_o_uri, uri_labels.get(same_as.get(nombre_o_uri, ""), nombre_o_uri))

for termino in ["París", "http://geo.example/city/paris", "París Hilton"]:
    print(termino, "->", resolver(termino))
```

- Pregunta de cierre (Misión 2)

¿Qué riesgo hay si enlazas owl:sameAs de más (falsos positivos)? Menciona un ejemplo concreto con nombres de la misión.

## Misión 3: Mini-grafo en Python y consultas tipo SPARQL

- La historia

Ya tienes un grafo en memoria: personas, libros y relaciones. Debes implementar un patrón de consulta por coincidencia de variables (como un BGP sencillo de SPARQL), no búsqueda por substring.

- Grafo base (completar con tus triples de la Misión 1 si quieres)

```python
# Representación: lista de dicts {s, p, o}
G = [
    {"s": "ex:alicia", "p": "tipo", "o": "ex:Persona"},
    {"s": "ex:alicia", "p": "nombre", "o": "Alicia García"},
    {"s": "ex:alicia", "p": "conoce", "o": "ex:bob"},
    {"s": "ex:bob", "p": "nombre", "o": "Bob Martínez"},
    {"s": "ex:bob", "p": "tipo", "o": "ex:Persona"},
    {"s": "ex:libro42", "p": "titulo", "o": "Introducción a la Web Semántica"},
    {"s": "ex:libro42", "p": "autor", "o": "ex:alicia"},
    {"s": "ex:libro42", "p": "autor", "o": "ex:bob"},
    {"s": "ex:libro42", "p": "anio", "o": "2019"},
]

def consulta_simple(g, patron):
    """
    patron: dict con claves s, p, o; valor None = variable (?)
    Devuelve lista de asignaciones {var: valor}
    """
    resultados = []
    for t in g:
        asignacion = {}
        ok = True
        for rol in ("s", "p", "o"):
            esperado = patron.get(rol)
            if esperado is None:
                continue
            if t[rol] != esperado:
                ok = False
                break
        if not ok:
            continue
        # registrar variables
        for rol in ("s", "p", "o"):
            if patron.get(rol) is None:
                asignacion[rol] = t[rol]
        if asignacion and asignacion not in resultados:
            resultados.append(asignacion)
    return resultados

# TAREA A: ¿Quiénes son autores del libro42? (patrón: ?persona autor ex:libro42)
patron_a = {"s": None, "p": "autor", "o": "ex:libro42"}
print("Autores:", consulta_simple(G, patron_a))

# TAREA B: Escribe un patrón que devuelva pares (persona, nombre)
# donde persona tiene tipo ex:Persona
# ESCRIBE patron_b y ejecuta:
# patron_b = ...
# print("Personas:", consulta_simple(G, patron_b))

# TAREA C: Añade un triple inferido manualmente:
# si X conoce Y y Y es tipo Persona, podrías catalogar X como "tieneConocidoPersona"
# (regla informal). Añade el triple a G y comenta qué haría un reasoner OWL real.
```

- Tu tarea
  - Completa patron_b y muestra la salida.
  - Responde: ¿en qué se parece consulta_simple a la cláusula WHERE de SPARQL? ¿en qué se queda corta?
  - Escribe la misma consulta de la Tarea A en pseudocódigo SPARQL (no hace falta endpoint real):

```python
# PREFIX ex: <http://ejemplo.org/>
# SELECT ?persona WHERE { ... }
```

## Misión 4 (opcional): Primer contacto con RDF en Python

Requiere: pip install rdflib

Carga los triples que diseñaste en la Misión 1 y ejecuta una consulta SELECT mínima.

```python
# Descomenta tras: pip install rdflib
# from rdflib import Graph, Namespace, Literal
# from rdflib.namespace import RDF
#
# EX = Namespace("http://ejemplo.org/")
# g = Graph()
# g.add((EX.alicia, EX.tieneNombre, Literal("Alicia García", lang="es")))
# ...
# for row in g.query("""SELECT ?n WHERE { ?p <http://ejemplo.org/tieneNombre> ?n }"""):
#     print(row)
```

## Entregable: Reporte previo (Markdown)

Entrega reporte_previa_web_semantica.md con:

```md
# Reporte — Actividad previa Web Semántica
**Estudiante:** [Nombre / matrícula]

## Misión 0 — Investigación
[Respuestas 1–3]

## Misión 1 — Triples desde HTML/JSON
[Lista de triples + problema de identidad duplicada]

## Misión 2 — URIs y París
[Tabla URI + sameAs + riesgos]

## Misión 3 — Mini-grafo
[Código patron_b, salidas, pseudocódigo SPARQL, reflexión vs SPARQL real]

## Puente al tema 5
Responde en 5–8 líneas: «¿Qué problema de esta actividad resuelve RDF que no resuelve solo JSON?»
```