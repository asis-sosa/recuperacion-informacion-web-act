# Descubrimiento y reutilización de los datos

Los datos del SIMANW pueden ser reutilizados por agentes externos sin necesidad de acceder al código fuente del sistema. Esto es posible porque el proyecto publica la información en formatos RDF estándar, utiliza vocabularios conocidos (Dublin Core, FOAF, Schema.org) y proporciona enlaces hacia recursos externos como Wikidata.

Un consumidor externo puede descargar el archivo Turtle o JSON-LD, cargarlo en un triple store y ejecutar consultas SPARQL directamente sobre los datos. También puede seguir enlaces owl:sameAs o skos:exactMatch para enriquecer la información mediante datasets públicos.

Gracias a la documentación de la ontología, cualquier desarrollador puede comprender el significado de las clases y propiedades sin inspeccionar la implementación interna. Esto favorece la interoperabilidad, la reutilización y la integración con otros sistemas de Web Semántica, cumpliendo los principios de Linked Open Data.
