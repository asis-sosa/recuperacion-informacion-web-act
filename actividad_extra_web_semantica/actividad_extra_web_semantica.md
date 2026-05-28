# Actividades extras Web Semántica (post-lectura)

Estas actividades van después de leer el material teórico actualizado y después (idealmente) de la actividad previa. No repiten el calentamiento inicial: aquí se comprueba que entiendes la nomenclatura, que puedes leer/escribir RDF y SPARQL, y que relacionas conceptos con situaciones reales.

**Prerrequisitos:**
- Haber leído al menos: introducción, «Glosario desde cero», secciones 5.1, 5.2 (RDF, RDFS, OWL, SPARQL) y 5.4 (datos abiertos).
- cPython 3; para misiones 5 y 6: pip install rdflib (opcional SPARQLWrapper para federación).

## Mapa de misiones

| Misión | Tema principal | Tiempo aprox |
|--------|----------------|--------------|
| A | Glosario y analogías | 25 min |
| B | Capas, OWA y SQL vs grafo	| 30 min |
| C | Turtle + inferencia RDFS	| 35 min |
| D | SPARQL (local o Wikidata)	| 40 min |
| E | Linked Data y 5 estrellas	| 25 min |
| F | Mini ontología + TBox/ABox | 35 min |
| G | SHACL vs reasoner (concepto) | 20 min |
| H | Proyecto integrador corto	| 45 min |

## Misión A: Comprueba el glosario (sin memorizar a ciegas)

**Instrucciones**
- Usa solo el documento web_semantica.org (sección «Glosario desde cero» y glosario final). No uses IA generativa para esta misión.
  1. Completa la tabla: escribe una frase en tus palabras (no copies la analogía literal del documento).

| Término | Tu definición (1 frase) | Ejemplo concreto (no del documento) |
|---------|-------------------------|-------------------------------------|
| URI | ... | ... |
| Triple | ... | ... |
| Literal | ... | ... |
| OWA | ... | ... |
| TBox | ... | ... |
| ABox | ... | ... |
| Endpoin t | ... | ... |
| LOD | ... | ... |

- Emparejamiento: une cada analogía del documento con el término correcto (escribe la letra).

```txt
a) ISBN de un libro
b) Plano urbanístico del conocimiento
c) SQL para redes de triples
d) Inspector de calidad en fábrica
e) No estar en mi lista de invitados ≠ no existir
f) Celda «34» en Excel, no un enlace

Términos: URI, Ontología, SPARQL, SHACL, OWA, Literal
```

- Pregunta corta: ¿Por qué una URL puede ser URI pero un URI con esquema urn:isbn:... no tiene por qué ser URL? (3 líneas máximo).

- Criterio de autoevaluación: Si en el ejemplo concreto usaste solo «Alicia» sin identificador global en la fila URI, revisa la sección «Principios de diseño» del material.

## Misión B: Capas, mundo abierto y comparación con SQL

- Parte 1 — Ordena las capas: Sin mirar la tabla del documento (cierra el archivo 2 minutos), intenta ordenar de abajo a arriba estas capas según Berners-Lee. Luego comprueba y corrige:
  - SPARQL, HTML, URI/IRI, OWL/RDFS, RDF
- Pregunta: ¿Por qué HTML está en la capa de «interfaz» y no en la de «sintaxis» de RDF? Relaciónalo con la analogía «biblioteca de folletos vs. fichas de catálogo».
- Parte 2 — OWA vs mundo cerrado: Lee el escenario y responde verdadero / falso / depende (mundo abierto) con justificación de una línea.

```txt
Base RDF de una universidad publicada en 2024. No aparece ningún triple:
  ex:maria rdf:type ex:Estudiante .

Preguntas:
1. ¿Se puede inferir que María NO es estudiante?
2. ¿Es lo mismo que una consulta SQL SELECT * FROM estudiantes WHERE id='maria' sin filas?
3. Si un reasoner OWL deduce ex:maria rdf:type ex:Persona porque ex:Estudiante rdfs:subClassOf ex:Persona y más tarde aparece ex:maria rdf:type ex:Estudiante, ¿invalida la inferencia anterior?
```

- Parte 3 — Tabla comparativa (completa tú)

| Pregunta | Web de documentos	| SQL típico | RDF + SPARQL |
|----------|--------------------|------------|--------------|
| Unidad básica	| ?	| ?	| ? |
| ¿Ausencia de dato implica falsedad? | ? | ? | ? |
| Identificador global típico | ? | ? | ? |
| Consulta declarativa | ? | ? | ? |

## Misión C: Escribir Turtle y ver inferencia RDFS

- Contexto: El dominio es un catálogo universitario mínimo. Debes usar prefijos y la sintaxis del documento (sección Turtle).

- Datos que debes modelar (hechos)
  - Alicia es Profesor; Bob es Estudiante.
  - Profesor es subclase de Persona; Estudiante es subclase de Persona.
  - Alicia enseña la asignatura Matemáticas I.
  - La propiedad :enseña tiene dominio Profesor y rango Asignatura.
  - El nombre de Alicia es «Alicia García» en español (@es).
- Tarea C1 — Archivo Turtle: Crea mentalmente o en un bloque Org el grafo en Turtle (mínimo 8 triples explícitos + tipos). Usa:

```org
@prefix ex: <http://ejemplo.org/uni#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# TU GRAFO AQUÍ (completa el estudiante)
```

- Tarea C2 — Inferencia en papel: Lista al menos 3 triples que un motor RDFS inferiría sin que los hayas escrito a mano (herencia de tipos, dominio/rango). Explica cada uno: «por regla X del documento, se deduce Y».

- Tarea C3 — Validación con rdflib (opcional recomendado)

```python
# pip install rdflib
# from rdflib import Graph
# g = Graph()
# g.parse("tu_archivo.ttl", format="turtle")  # o parse data= string
# print(len(g)), "triples cargados"
# Compara: triples explícitos vs g con RDFS reasoning si tu versión lo soporta
```

- Pregunta de cierre C: ¿Qué diferencia hay entre «poner rdfs:subClassOf en el TBox» y «poner rdf:type Profesor en el ABox»? Usa la analogía TBox/ABox del glosario.

## Misión D: Consultas SPARQL

- D1 — Sobre tu grafo de la Misión C (local): Escribe tres consultas y resultado esperado en prosa (no hace falta ejecutar si no tienes rdflib):
  1. SELECT: nombres de todas las Personas (inferidas o explícitas).
  2. ASK: ¿Bob es subtipo de Persona? (¿qué devuelve true/false?)
  3. SELECT con FILTER: profesores cuyo nombre está en idioma español.

```python
PREFIX ex: <http://ejemplo.org/uni#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# Consulta 1
# SELECT ...

# Consulta 2
# ASK ...

# Consulta 3
# SELECT ... FILTER ...
```

- D2 — Wikidata Query Service (en línea): Abre https://query.wikidata.org/ y ejecuta una consulta que devuelva al menos 5 filas. Opciones (elige una):
  - Museos en México con coordenadas.
  - Películas de un director que elijas.
  - Ciudades que son capital de un país de América Latina.

- Entrega:
  - La consulta SPARQL pegada.
  - Captura o descripción de 2 columnas del resultado.
  - ¿Qué IRIs ves en la respuesta (ej. wd:Q...)? ¿Por qué Wikidata usa URIs y no solo nombres?

- D3 — Puente con la actividad previa: Reescribe en SPARQL real la «Tarea A» de la Misión 3 de web_semantica_actividad_previa.org (autores de ex:libro42). Compara con tu función consulta_simple: ¿qué cláusula SPARQL no implementaste en Python?

## Misión E: Linked Data, JSON-LD y datos abiertos

- E1 — Cuatro principios en la práctica: Para un dataset hipotético «Bibliotecas de México»:

| Principio Linked Data | ¿Cómo lo cumplirías? (1 línea) | ¿Qué pasa si NO lo cumples? |
|-----------------------|--------------------------------|-----------------------------|
| 1. URIs como nombres | ... | ... |
| 2. URIs HTTP | ... | ... |
| 3. Content negotiation | ... | ... |
| 4. Enlaces a otros LOD | ... | ... |

- E2 — Subir en las 5 estrellas: Un municipio publica un PDF con tabla escaneada de presupuesto. Clasifica en ★ a ★★★★★ y propón dos pasos concretos para subir al menos dos estrellas.

- E3 — JSON-LD embebido (lectura): Pega un fragmento inventado de <script type"application/ld+json">= para un evento cultural (usa @context con schema.org). Indica qué triples RDF equivaldrían (sujeto, predicado, objeto en español).

```python
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Feria del Libro",
  "startDate": "2026-11-01",
  "location": {
    "@type": "Place",
    "name": "Centro Histórico"
  }
}
```

- Pregunta E3: ¿El @context cumple la misma función que PREFIX en Turtle? Explica en 2–3 líneas.

## Misión F: Diseño TBox / ABox (mini ontología)

- Escenario: Una app de recomendación de cursos en línea necesita interoperar con otra universidad. Diseña en papel (o Turtle solo TBox) lo siguiente:
  - Al menos 3 clases con jerarquía (rdfs:subClassOf).
  - Al menos 2 propiedades con rdfs:domain y rdfs:range.
  - Una restricción que solo se puede expresar bien en OWL, no en RDFS puro (ej. owl:FunctionalProperty, cardinalidad min 1). Escríbela en Turtle con prefijo owl:.
  - Escribe 5 triples ABox de individuos ficticios que respeten tu TBox.
- Pregunta F: ¿Qué vocabulario reutilizarías del documento (schema.org, FOAF, DCAT, SKOS) y para qué campo concreto de tu app? Mínimo dos vocabularios con justificación.

## Misión G: SHACL vs Reasoner (conceptual + mini ejercicio)

- G1 — Diferencia en criollo, Completa:
  - El reasoner OWL/RDFS añade conocimiento porque …
  - SHACL no inventa triples; en su lugar …
- G2 — Detecta el error, Este grafo dice:

```org
ex:ana rdf:type ex:Persona .
ex:ana ex:email "ana@uni.edu" .
ex:ana ex:email "ana.personal@gmail.com" .
```

- Y la forma SHACL dice: «cada ex:Persona tiene como máximo un ex:email».
  - ¿El grafo viola SHACL?
  - ¿Un reasoner RDFS inferiría algo sobre los dos emails? (pista: necesitas owl:FunctionalProperty en el TBox)
  - ¿Qué herramienta usarías antes de publicar el dataset en un portal LOD?

## Misión H: Proyecto integrador «Del dato abierto al grafo»

- Historia: Tu equipo debe integrar dos fuentes para un panel «Quién enseña qué y dónde está el campus»:

```python
fuente_tabla = [
    {"id_interno": "P1", "nombre": "Dr. Luis Méndez", "materia": "Física I"},
    {"id_interno": "P2", "nombre": "Dra. Carmen Ruiz", "materia": "Química"},
]

fuente_rdf_snippet = """
@prefix ex: <http://campus.ejemplo/edificios#> .
ex:edificioNorte ex:tieneNombre "Edificio Norte"@es .
ex:aula301 ex:estaEn ex:edificioNorte .
"""
```

- Entregables de la Misión H
  - Diseño: IRIs propuestas para profesores, materias y edificios (tabla nombre legible → IRI).
  - Al menos 12 triples Turtle unificados (puedes enlazar profesor ↔ materia ↔ aula).
  - Una consulta SPARQL que responda: «¿Qué materias se imparten en el Edificio Norte?» (aunque la tabla original no mencionaba edificios).
  - Un enlace LOD: propón skos:exactMatch o owl:sameAs hacia un recurso Wikidata (IRI wd:...) para una entidad (materia, ciudad o institución).
  - Reflexión (8–10 líneas): ¿Qué parte de este ejercicio sería imposible solo con búsqueda por keywords en HTML?

## Entregable único: Reporte en Markdown

```md
# Reporte — Actividades extras Web Semántica
**Estudiante:** [Nombre / matrícula]
**Fecha:**

## Misión A — Glosario
[Tabla + emparejamiento + URI vs URL]

## Misión B — Capas y OWA
[Orden capas + respuestas OWA + tabla comparativa]

## Misión C — Turtle y RDFS
[Código Turtle + triples inferidos + reflexión TBox/ABox]

## Misión D — SPARQL
[3 consultas locales + Wikidata + puente actividad previa]

## Misión E — Linked Data
[Tabla 4 principios + 5 estrellas + JSON-LD]

## Misión F — Mini ontología
[TBox + ABox + vocabularios reutilizados]

## Misión G — SHACL vs reasoner
[Completar frases + caso dos emails]

## Misión H — Integración
[IRIs + Turtle + SPARQL + sameAs + reflexión]

## Síntesis final (obligatoria)
Responde: «Si mañana desaparecieran los estándares W3C de RDF/SPARQL, ¿qué perdería concretamente
el proyecto de la Misión H que sí tendría con solo APIs REST + JSON?»
```