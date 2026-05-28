# Reporte — Actividades extras Web Semántica

**Estudiante:** Sebastian Asis Sosa Santiago / 22120720

**27 / 05 / 2026**

## Misión A — Glosario

**A1**

| Término | Tu definición | Ejemplo concreto |
|---------|---------------|------------------|
| URI | Es un identificador clave, unico que defina la direccion de la informacion | https://wwww.mexico-global.com |
| Triple | Es una forma de estructura en que se puede relacionar ciertos aspectos | Alicia - EsAmiga - Pablo |
| Literal | Es un dato comun hecho en cualquier tipo de formato, como por ejemplo texto sin formato | Yo me llamo Sebastian |
| OWA | En el mundo de la tecnologia, si cierta informacion no esta presente, no se da por hecho de que no exista | Una base de datos aun en desarrollo |
| TBox | Es donde se definen ciertas reglas que sigue la informacion para su mejor entendimiento | Definir un doctor como un tipo de persona |
| ABox | Son datos que se podrian considerar como concretos o reales | Alicia es Doctora |
| Endpoint | Es una clase de servicio donde se es posible realizar consultas | En un registro donde se permita visualizar las consultas |
| LOD | Son datos que pueden estar conectados con otros de distintas fuentes | Los datos que ofrece el INEGI sobre diversos elementos que tienen que ver con el pais Mexicano |

**A2**

| Analogia | Termino Correcto |
|----------|------------------|
| ISBN de un libro | URI |
| Plano urbanístico del conocimiento | Ontología |
| SQL para redes de triples | SPARQL |
| Inspector de calidad en fábrica | SHACL |
| No estar en mi lista de invitados ≠ no existir | OWA |
| Celda «34» en Excel, no un enlace | Literal |

**A3**

**Pregunta corta:** ¿Por qué una URL puede ser URI pero un URI con esquema urn:isbn:... no tiene por qué ser URL? (3 líneas máximo).

Porque un URL es una clase de identificador que no solo define esta estructura de identificador, sino que tambien indica la manera de acceder a este recurso, cosa que el URI no cuenta del todo y mucho menos cuando se define en el esquema "urn:isbn...", que es aqui donde el URI solo identifica algo, mas no indica la manera de acceder a el, por lo tanto un URL puede ser considero un URI como tal, pero este no puede considerarse un URL.

## Misión B — Capas y OWA

**B1**

| Capa | Tecnologia |
|----------|------------------|
| Identificadores | URI/IRI |
| Sintaxis | RDF |
| Esquema | OWL/RDFS |
| Consulta | SPARQL |
| Interfaz | HTML |

**Pregunta:** ¿Por qué HTML está en la capa de «interfaz» y no en la de «sintaxis» de RDF? Relaciónalo con la analogía «biblioteca de folletos vs. fichas de catálogo».

Porque HTML es utilizado y esta enfocado en mostrar, visualmente al usuario la informacion que existe en la pagina, mientras que RDF esta enfocado en describir el significado claro de los datos, por lo que si se llegase a utilizar una analogia, HTML seria como una biblioteca de folletos, los cuales son los que aprecian los usuarios y donde adquieren la informacion, por otro lado, con la analogia de las fichas de catalogo seria el RDF, ya que estas son las que organizan la informacion.

**B2**

**Preguntas:**
1. ¿Se puede inferir que María NO es estudiante?

Falso - Ya que la base funciona con RDF que se considero como un mundo abierto, la base funciona como un OWA, por lo que, aunque no este, puede existir en la base

2. ¿Es lo mismo que una consulta SQL SELECT * FROM estudiantes WHERE id='maria' sin filas?

Verdadero - Ya que esta consulta arrojara una tabla temporal donde muestre los estudiantes que cumple con la condicion, como maria no esta presente, se mostrara la tabla sin filas.

3. Si un reasoner OWL deduce ex:maria rdf:type ex:Persona porque ex:Estudiante rdfs:subClassOf ex:Persona y más tarde aparece ex:maria rdf:type ex:Estudiante, ¿invalida la inferencia anterior?

Falso - Esto solo valida la deduccion por parte del OWL al definir a maria como Persona, ya que se esta relacionando que un estudiante es una persona.

**B3**

| Pregunta | Web de documentos	| SQL típico | RDF + SPARQL |
|----------|--------------------|------------|--------------|
| Unidad básica	| Paginas de infromacion | Los registro de cada tabla | Los tiples o estructura de relacion de datos |
| ¿Ausencia de dato implica falsedad? | No del todo, puede haber verdad en lo poco | Si por la falta de informacion en la base | No porque trata con hechos |
| Identificador global típico | Los URLs | Llaves primarias o IDs | Las URIs |
| Consulta declarativa | Buscador interno | El mismo SQL | El mismo SPARQL |

## Misión C — Turtle y RDFS

**C1**

```org
@prefix ex: <http://ejemplo.org/uni#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Alicia rdf:type ex:Profesor .
ex:Bob rdf:type ex:Estudiante .

ex:Profesor rdfs:subClassOf ex:Persona .
ex:Estudiante rdfs:subClassOf ex:Persona .

ex:MatematicasI rdf:type ex:Asignatura .

ex:Alicia ex:enseña ex:MatematicasI .

ex:enseña rdfs:domain ex:Profesor .
ex:enseña rdfs:range ex:Asignatura .

ex:Alicia ex:nombre "Alicia García"@es .
```

**C2**

```org
ex:Alicia rdf:type ex:Persona .
```
Aqui se hace la inferencia de que "Alicia" es una "persona", debido a que "profesor" es una "persona" y como "Alicia" es una "profesora" se deduce la inferncia

```org
ex:Bob rdf:type ex:Persona .
```
Mismo caso que con el de "Alicia" solo que ahora cambias el tiple de "profesor" a "estudiante" y regla es la misma.

```org
ex:Alicia rdf:type ex:Profesor .
```
Aqui la inferencia esta relacionada al dominio entre "enseña", "profesor" y el rango de "enseña" y "asignatura" es que se puede determinar que "Alicia" es "profesor" por la asignatura que imparte

**C3**

```python
from rdflib import Graph

ttl = """
@prefix ex: <http://ejemplo.org/uni#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Alicia rdf:type ex:Profesor .
ex:Bob rdf:type ex:Estudiante .

ex:Profesor rdfs:subClassOf ex:Persona .
ex:Estudiante rdfs:subClassOf ex:Persona .

ex:MatematicasI rdf:type ex:Asignatura .

ex:Alicia ex:enseña ex:MatematicasI .

ex:enseña rdfs:domain ex:Profesor .
ex:enseña rdfs:range ex:Asignatura .

ex:Alicia ex:nombre "Alicia García"@es .
"""

g = Graph()
g.parse(data=ttl, format="turtle")

print(len(g), "triples cargados")
```

**Pregunta de cierre C:** ¿Qué diferencia hay entre «poner rdfs:subClassOf en el TBox» y «poner rdf:type Profesor en el ABox»? Usa la analogía TBox/ABox del glosario.

La diferencia entre ambos consiste en que, TBox define las categorias y las relaciones generales que hay en los triples, por ejemplo las reglas que define un cliente como persona, para el caso del ABox se tiene los hechos concretos de los individuos, como relacionar la persona Juan perez como un cliente.

## Misión D — SPARQL

**D1**

```python
PREFIX ex: <http://ejemplo.org/uni#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# Consulta 1
SELECT ?persona ?nombre
WHERE {
  ?persona rdf:type ex:Persona .
  OPTIONAL { ?persona ex:nombre ?nombre . }
}

# Consulta 2
ASK {
  ex:Bob rdf:type ex:Persona .
}

# Consulta 3
SELECT ?profesor ?nombre
WHERE {
  ?profesor rdf:type ex:Profesor .
  ?profesor ex:nombre ?nombre .
  FILTER(lang(?nombre) = "es")
}
```

**Consulta 1 Resultado Esperado**

Se espera que el motor aplique inferencias, indicando a Alicia como Alicia Garcia, mientras que Bob apareceria sin nombre

**Consulta 2 Resultado Esperado**

Es probale que si hubiera inferencia, el resultado arrojaria Verdadero, porque Bob es estudiante y estudiante pertenece a persona. Si no hubiera inferencia, arrojaria falso.

**Consulta 3 Resultado Esperado**

Arrojaria del ejemplo de Alicia con el nombre Alicia Garcia.

**D2**

```sql
SELECT ?museo ?museoLabel ?coord
WHERE {
  ?museo wdt:P31/wdt:P279* wd:Q33506;
         wdt:P17 wd:Q96;
         wdt:P625 ?coord.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 5
```

| museo | museoLabel | coord |
|-------|------------|-------|
| wd:Q5654473 | Museo Ex Teresa Arte Actual	| Point (-99.13075 19.43403) |
| wd:Q5675425 | Pinacoteca Universitaria Alfonso Michel	| Point (-103.72624 19.24491) |
| wd:Q5677940 | Museo de Historia Natural José Narciso Rovirosa	| Point (-92.92805556 17.98916667) |
| wd:Q5692713 | Museo del Automóvil	| Point (-99.139166666 19.324166666) |
| wd:Q5702991 | Archivo Histórico y Museo de Minería de Pachuca	| Point (-98.73127 20.12543) |

**D3**

```sarql
PREFIX ex: <http://ejemplo.org/biblio#>

SELECT ?autor
WHERE {
  ex:libro42 ex:autor ?autor .
}
```

**Pregunta:** ¿qué cláusula SPARQL no implementaste en Python?

Algunas de las calusulas de SPARQL que no se implementaron en python se encuentran "FILTER", "OPTIONAL", "ORDER BY", "LIMIT" entre otras mas.

## Misión E — Linked Data

**E1**

| Principio Linked Data | ¿Cómo lo cumplirías? | ¿Qué pasa si NO lo cumples? |
|-----------------------|----------------------|-----------------------------|
| 1. URIs como nombres | Aplicaria URIs unicos a cada biblioteca. | Es muy posible que los datos lleguen a confundirse por la falta de identificadores unicos. |
| 2. URIs HTTP | utilizaria direcciones como https://datos.gob.mx/bibliotecas/123 para definir adecuadamente las rutas. | Otros sistemas no podrian acceder a los recursos. |
| 3. Content negotiation | Lograria que el mismo URI entregue HTML para usuarios y RDF para las maquinas. | Los datos serian menos reutilizables por aplicaciones. |
| 4. Enlaces a otros LOD | Haria la coneccion de bibliotecas con Wikidata o datos oficiales de municipios. | El dataset seria aislado y sería menos útil. |

**E2**

Un PDF con una tabla escaneada aproximadamente tendria entre 1 a 2 estrellas, esto debido a que no estaria facilmente procesable por una computadora, es muy probable que lo que le podria agregar mas valor seria poder convertir la tabla a un archivo estructurado como CSV, ademas de publicarlo con una licencia abierta y con datos reutilizables.

**E3**

```html
<script type="application/ld+json">
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
</script>
```

| Sujeto           | Predicado       | Objeto             |
| ---------------- | --------------- | ------------------ |
| Evento cultural  | tipo            | Event              |
| Evento cultural  | nombre          | “Feria del Libro”  |
| Evento cultural  | fecha de inicio | “2026-11-01”       |
| Evento cultural  | ubicación       | Centro Histórico   |
| Centro Histórico | tipo            | Place              |
| Centro Histórico | nombre          | “Centro Histórico” |

**Pregunta:** ¿El @context cumple la misma función que PREFIX en Turtle? Explica en 2–3 líneas.

Si ambas cumple la misma funcion, esto es debido a que ambas permiten abreviar vocabularios y notificar de donde provienen ciertos terminos como en el script anterior con "name", "Event" o inclusive "location". Si se llegasen a diferenciar, "@context" trabaja dentro de JSON-LD, mientras que con "PREFIX" se trabaja con Turtle o SPARQL.

## Misión F — Mini ontología

```ttl
@prefix ex: <http://ejemplo.org/cursos#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

# Clases
ex:Curso rdf:type rdfs:Class .
ex:CursoProgramacion rdf:type rdfs:Class ;
    rdfs:subClassOf ex:Curso .

ex:CursoBaseDatos rdf:type rdfs:Class ;
    rdfs:subClassOf ex:Curso .

ex:Persona rdf:type rdfs:Class .
ex:Estudiante rdf:type rdfs:Class ;
    rdfs:subClassOf ex:Persona .

ex:Instructor rdf:type rdfs:Class ;
    rdfs:subClassOf ex:Persona .

# Propiedades
ex:imparte rdf:type rdf:Property ;
    rdfs:domain ex:Instructor ;
    rdfs:range ex:Curso .

ex:inscritoEn rdf:type rdf:Property ;
    rdfs:domain ex:Estudiante ;
    rdfs:range ex:Curso .

# Restricción OWL
ex:correoInstitucional rdf:type owl:FunctionalProperty ;
    rdfs:domain ex:Persona ;
    rdfs:range rdfs:Literal .
```

```ttl
ex:Ana rdf:type ex:Estudiante .
ex:DrLopez rdf:type ex:Instructor .
ex:PythonBasico rdf:type ex:CursoProgramacion .
ex:Ana ex:inscritoEn ex:PythonBasico .
ex:DrLopez ex:imparte ex:PythonBasico .
```

**Pregunta F:** ¿Qué vocabulario reutilizarías del documento (schema.org, FOAF, DCAT, SKOS) y para qué campo concreto de tu app? Mínimo dos vocabularios con justificación.

Lo mas probable es que volveria a utilizar el documento "schema.org" porque me permitiria describir recursos, nombres, fechas y demas elementos que ya tienen un vocabulario comun para los contenidos educativos y / o de eventos, de igual manera utilizaria "FOAF" para representar personas como estudiantes o instructores, inclusive podriar llegar a usar "SKOS" para organizar temas o categorias de cursos.

## Misión G — SHACL vs reasoner

**G1**

- El reasoner OWL/RDFS añade conocimiento porque utiliza reglas de la ontologia para deducir nuevos triples que no estaban escritos explicitamente.
- SHACL no inventa triples; en su lugar revisa si los datos cumplen reglas de validacion, como campos obligatorios, tipos correctos o cantidad máxima de valores.

**G2**

- ¿El grafo viola SHACL?

Asi es, el grafo viola completamente SHACL, ya que "Ana" es una "Persona" y esta tiene dos valores para "email", pero la manera de SHACL indica que cada "Persona" debe tener maximo un "email"

- ¿Un reasoner RDFS inferiría algo sobre los dos emails?

No, un reasoner RDFS no determina por si solo que sea una clase de error, ni de que los dos "emails" deben ser totalmente iguales.

- ¿Qué herramienta usarías antes de publicar el dataset en un portal LOD?

Antes de siquiera publicar un dataset validaria con SHACL, ya que este permite detectar los datos incompletos, los que estan repetidos o mal estructurados.

## Misión H — Integración

| Nombre legible   | IRI propuesta        |
| ---------------- | -------------------- |
| Dr. Luis Méndez  | `exprof:P1`          |
| Dra. Carmen Ruiz | `exprof:P2`          |
| Física I         | `exmat:FisicaI`      |
| Química          | `exmat:Quimica`      |
| Aula 301         | `exed:aula301`       |
| Edificio Norte   | `exed:edificioNorte` |

```ttl
@prefix exprof: <http://universidad.ejemplo/profesores#> .
@prefix exmat: <http://universidad.ejemplo/materias#> .
@prefix exed: <http://campus.ejemplo/edificios#> .
@prefix ex: <http://universidad.ejemplo/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix wd: <http://www.wikidata.org/entity/> .

exprof:P1 rdf:type ex:Profesor .
exprof:P1 ex:nombre "Dr. Luis Méndez"@es .
exprof:P1 ex:enseña exmat:FisicaI .

exprof:P2 rdf:type ex:Profesor .
exprof:P2 ex:nombre "Dra. Carmen Ruiz"@es .
exprof:P2 ex:enseña exmat:Quimica .

exmat:FisicaI rdf:type ex:Materia .
exmat:FisicaI ex:nombre "Física I"@es .
exmat:FisicaI ex:seImparteEn exed:aula301 .

exmat:Quimica rdf:type ex:Materia .
exmat:Quimica ex:nombre "Química"@es .
exmat:Quimica ex:seImparteEn exed:aula301 .

exed:aula301 rdf:type ex:Aula .
exed:aula301 ex:tieneNombre "Aula 301"@es .
exed:aula301 ex:estaEn exed:edificioNorte .

exed:edificioNorte rdf:type ex:Edificio .
exed:edificioNorte ex:tieneNombre "Edificio Norte"@es .

exmat:Quimica skos:exactMatch wd:Q2329 .
```

**Pregunta:** ¿Qué materias se imparten en el Edificio Norte?

```sparql
PREFIX exmat: <http://universidad.ejemplo/materias#>
PREFIX exed: <http://campus.ejemplo/edificios#>
PREFIX ex: <http://universidad.ejemplo/vocab#>

SELECT ?materia ?nombreMateria
WHERE {
  ?materia ex:seImparteEn ?aula .
  ?aula ex:estaEn exed:edificioNorte .
  ?materia ex:nombre ?nombreMateria .
}
```

```ttl
exmat:Quimica skos:exactMatch wd:Q2329 .
```

**Reflexion:** ¿Qué parte de este ejercicio sería imposible solo con búsqueda por keywords en HTML?

El uso de las keywords o palabras clave, se podrian considerar bastante buenas para hacer busquedas en relacion a esas palabras, pero seria realmente dificil poder unir correctamente cierta informacion con otra, como es el caso de las activiades anteriores, donde seria complicado determinar relacion entre profesores, materias, aulas, etc entre si, un ejemplo seria que una buscqueda con estas palabras clave diera con la materia o el aula, pero no daria automaticamente con el profesor que imparte la materia o que se ubique en el aula, utilizando RDF estas relaciones quedan explicitas mediante el uso de los triples, creando el camino de consulta en relacion al profesor, material, aula y el edificio, inclusive las IRIs pueden evitar confusiones entre los casos de que hubiera nombres muy parecidos, permitiendo integrar datos de diferentes fuentes. Se podria decir que su mayor ventaja de los RDFs es entender las relaciones entre entidades, es quizas por esa razon que SPARQL puede responder preguntas que no se encontraban literalmente escritas en una tabla originalmente.

## Síntesis final (obligatoria)

Responde: «Si mañana desaparecieran los estándares W3C de RDF/SPARQL, ¿qué perdería concretamente el proyecto de la Misión H que sí tendría con solo APIs REST + JSON?»

Si el dia de mañana desaparecieran estos estandares, la mision perderia mayormente su capacidad de representar las relaciones estandarizadas que hay los profesores, las materias, las aulas e inclusive los edificios, el uso de APIs REST y JSON aun podria facilitar un poco el intercambio de datos, sin embargo, cada sistema tendria sus propios formatos y estructuras que dificultarian la compatibilidad entre instituciones, de igual manera se perderia la posibilidad de realizar consultas complejas con el uso de SPARQL, donde se es posible recorrer multiples relaciones que hay presentes en el grafo, otro punto es que, el RDF permite utilizar los URIs globales y de cierta manera enlazar las entidades con los recursos externos.