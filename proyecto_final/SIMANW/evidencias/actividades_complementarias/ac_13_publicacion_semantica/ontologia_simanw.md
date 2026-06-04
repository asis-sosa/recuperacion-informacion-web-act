# Ontología del SIMANW

## Prefijos utilizados

| Prefijo | URI                              |
| ------- | -------------------------------- |
| simanw  | http://simanw.org/ontology/      |
| data    | http://simanw.org/data/          |
| dc      | http://purl.org/dc/elements/1.1/ |
| foaf    | http://xmlns.com/foaf/0.1/       |
| schema  | https://schema.org/              |

## Clases

### simanw:Noticia

Representa una noticia almacenada por el sistema.

### simanw:Autor

Representa al autor de una noticia.

### simanw:Categoria

Representa una categoría temática asignada a una noticia.

### simanw:Fuente

Representa el origen de una noticia.

## Propiedades

### simanw:tieneAutor

Relaciona una noticia con su autor.

### simanw:tieneCategoria

Relaciona una noticia con una categoría.

### simanw:sentimientoEtiqueta

Indica la clasificación de sentimiento.

### simanw:sentimientoScore

Indica la puntuación numérica del sentimiento.

### simanw:urlOriginal

Enlace a la noticia original.

### simanw:provieneDe

Relaciona una noticia con una fuente.

## Objetivo

Permitir la representación semántica de noticias procesadas por el SIMANW para su consulta mediante RDF y SPARQL.
