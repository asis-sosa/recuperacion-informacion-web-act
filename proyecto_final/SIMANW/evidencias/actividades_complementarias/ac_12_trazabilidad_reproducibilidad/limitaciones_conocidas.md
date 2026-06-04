# Limitaciones conocidas del SIMANW

## Cambios en sitios rastreados

El rastreador depende de la estructura HTML de los portales de noticias. Si cambian los selectores o la organización del sitio, será necesario actualizar el código de extracción.

## Disponibilidad de Internet

Las consultas SPARQL externas (Wikidata, DBpedia) requieren conectividad y disponibilidad de los endpoints públicos.

## Calidad de las noticias

La calidad del análisis depende directamente de la calidad del corpus rastreado. Noticias incompletas o con errores afectan la clasificación y el análisis posterior.

## Escalabilidad

La implementación académica fue diseñada para corpus pequeños y medianos. Para millones de documentos sería necesario utilizar bases de datos especializadas e índices distribuidos.

## Análisis semántico

El sistema utiliza técnicas estadísticas y modelos tradicionales. No incorpora modelos LLM ni embeddings modernos, por lo que algunas consultas complejas pueden producir resultados limitados.

## Clasificación automática

Las categorías predichas pueden contener errores cuando una noticia aborda múltiples temas simultáneamente.

## Dependencias externas

Las bibliotecas Python utilizadas pueden cambiar entre versiones, por lo que se recomienda mantener un archivo requirements.txt con versiones fijas para garantizar la reproducibilidad.
