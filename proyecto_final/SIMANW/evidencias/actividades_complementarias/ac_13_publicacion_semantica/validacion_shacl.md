# Validación del Knowledge Graph

## Restricciones definidas

### NoticiaShape

Toda noticia debe contener:

* Título
* Fecha
* Categoría
* URL

### AutorShape

Todo autor debe tener:

* Nombre

## Violaciones encontradas

| Recurso    | Violación          |
| ---------- | ------------------ |
| noticia_17 | Fecha faltante     |
| noticia_23 | Categoría faltante |

## Correcciones aplicadas

* Se completó la fecha utilizando los metadatos originales del rastreo.
* Se reclasificó automáticamente la noticia sin categoría.

## Resultado final

Tras la corrección:

* Violaciones iniciales: 2
* Violaciones finales: 0

El grafo cumple las restricciones definidas.
