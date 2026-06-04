# Consultas SPARQL propias

## Consulta 1

Pregunta de negocio:

¿Qué autores publicaron noticias con sentimiento negativo?

```sparql
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?autor
WHERE {
  ?n simanw:tieneAutor ?a .
  ?a foaf:name ?autor .
  ?n simanw:sentimientoEtiqueta "negativo" .
}
```

## Consulta 2

Pregunta de negocio:

¿Cuántas noticias existen por categoría?

```sparql
PREFIX simanw: <http://simanw.org/ontology/>

SELECT ?categoria (COUNT(?n) AS ?total)
WHERE {
  ?n simanw:tieneCategoria ?categoria .
}
GROUP BY ?categoria
```

## Consulta 3

Pregunta de negocio:

¿Qué noticias relacionadas con tecnología tienen enlaces externos?

```sparql
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?noticia ?enlace
WHERE {
  ?noticia simanw:tieneCategoria ?c .
  ?c owl:sameAs ?enlace .
}
```
