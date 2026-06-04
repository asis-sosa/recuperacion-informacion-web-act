from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF, SKOS

class KnowledgeGraphSIMANW:
    def __init__(self):
        self.graph = Graph()

        self.NS = Namespace("http://simanw.org/ontology/")
        self.DATA = Namespace("http://simanw.org/data/")

        self.graph.bind("simanw", self.NS)
        self.graph.bind("data", self.DATA)
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)

        self._definir_ontologia()

    def _definir_ontologia(self):
        self.graph.add((self.NS.Noticia, RDF.type, OWL.Class))
        self.graph.add((self.NS.Autor, RDF.type, OWL.Class))
        self.graph.add((self.NS.Categoria, RDF.type, OWL.Class))
        self.graph.add((self.NS.Fuente, RDF.type, OWL.Class))

        self.graph.add((self.NS.tieneAutor, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.tieneAutor, RDFS.domain, self.NS.Noticia))
        self.graph.add((self.NS.tieneAutor, RDFS.range, self.NS.Autor))

        self.graph.add((self.NS.tieneCategoria, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.provieneDe, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.relacionadaCon, RDF.type, OWL.ObjectProperty))

        self.graph.add((self.NS.sentimientoScore, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.sentimientoEtiqueta, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.urlOriginal, RDF.type, OWL.DatatypeProperty))

    def agregar_noticia(self, noticia, noticia_id):
        uri = self.DATA[f"noticia_{noticia_id}"]

        self.graph.add((uri, RDF.type, self.NS.Noticia))
        self.graph.add((uri, DC.title, Literal(noticia["titulo"], lang="es")))
        self.graph.add((uri, DC.description, Literal(noticia["cuerpo"][:200], lang="es")))
        self.graph.add((uri, DC.date, Literal(noticia["fecha"], datatype=XSD.date)))

        autor_uri = self.DATA[f"autor_{noticia['autor'].replace(' ', '_')}"]
        self.graph.add((autor_uri, RDF.type, self.NS.Autor))
        self.graph.add((autor_uri, FOAF.name, Literal(noticia["autor"])))
        self.graph.add((uri, self.NS.tieneAutor, autor_uri))

        categoria = noticia.get("categoria_predicha", noticia.get("categoria_original", "general"))
        cat_uri = self.DATA[f"categoria_{categoria}"]

        self.graph.add((cat_uri, RDF.type, self.NS.Categoria))
        self.graph.add((cat_uri, RDFS.label, Literal(categoria, lang="es")))
        self.graph.add((uri, self.NS.tieneCategoria, cat_uri))

        if "sentimiento" in noticia:
            sent = noticia["sentimiento"]

            self.graph.add((
                uri,
                self.NS.sentimientoScore,
                Literal(sent["compound"], datatype=XSD.float)
            ))

            self.graph.add((
                uri,
                self.NS.sentimientoEtiqueta,
                Literal(sent["etiqueta"])
            ))

        if "url" in noticia:
            self.graph.add((
                uri,
                self.NS.urlOriginal,
                Literal(noticia["url"], datatype=XSD.anyURI)
            ))

    def consultar(self, sparql_query):
        return list(self.graph.query(sparql_query))

    def total_triples(self):
        return len(self.graph)

    def serializar(self, formato="turtle"):
        return self.graph.serialize(format=formato)


kg = KnowledgeGraphSIMANW()

class EnriquecedorKG:
    """
    AC-7: Enriquece el KG local conectando con Wikidata/DBpedia.
    El alumno debe ejecutar consultas reales a endpoints SPARQL.
    """

    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.WD = Namespace("http://www.wikidata.org/entity/")
        self.WDT = Namespace("http://www.wikidata.org/prop/direct/")
        self.kg.graph.bind("wd", self.WD)
        self.kg.graph.bind("wdt", self.WDT)
        self.enlaces_externos = []

    def enlazar_entidad(self, entidad_local, wikidata_id, etiqueta):
        """Enlaza una entidad local con su equivalente en Wikidata."""
        self.kg.graph.add((entidad_local, OWL.sameAs, self.WD[wikidata_id]))
        self.kg.graph.add((entidad_local, SKOS.exactMatch, self.WD[wikidata_id]))
        self.kg.graph.add((self.WD[wikidata_id], RDFS.label, Literal(etiqueta, lang="es")))
        self.enlaces_externos.append({
            'local': str(entidad_local),
            'wikidata': wikidata_id,
            'etiqueta': etiqueta
        })

    def agregar_datos_externos(self, entidad_local, propiedades):
        """Agrega propiedades obtenidas de fuentes externas."""
        for prop, valor in propiedades.items():
            self.kg.graph.add((entidad_local, self.WDT[prop], Literal(valor)))

    def consulta_enriquecimiento(self):
        """Query SPARQL para verificar enlaces externos."""
        query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT ?local ?externo ?etiqueta
        WHERE {
            ?local owl:sameAs ?externo .
            ?externo rdfs:label ?etiqueta .
        }
        """
        return list(self.kg.graph.query(query))

    def generar_query_wikidata(self, tema):
        """Genera consultas SPARQL para Wikidata según el tema."""
        queries = {
            'tecnologia': """
# Consulta: Herramientas de NLP en Wikidata
SELECT ?item ?itemLabel ?description WHERE {
  ?item wdt:P31 wd:Q7397 .          # instancia de software
  ?item wdt:P366 wd:Q30642 .        # uso: NLP
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 10""",
            'ciencia': """
# Consulta: Investigaciones sobre cambio climático
SELECT ?item ?itemLabel ?date WHERE {
  ?item wdt:P31 wd:Q13442814 .      # instancia de artículo científico
  ?item wdt:P921 wd:Q7942 .         # tema: cambio climático
  ?item wdt:P577 ?date .
  FILTER(YEAR(?date) >= 2024)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 10""",
        }
        return queries.get(tema, "# No hay consulta predefinida para este tema")


# Enriquecer el KG del SIMANW
enriquecedor = EnriquecedorKG(kg)

# Enlazar categorías con Wikidata
DATA = Namespace("http://simanw.org/data/")
enriquecedor.enlazar_entidad(DATA["categoria_tecnologia"], "Q11016", "Tecnología de la información")
enriquecedor.enlazar_entidad(DATA["categoria_economia"], "Q159810", "Economía")
enriquecedor.enlazar_entidad(DATA["categoria_ciencia"], "Q336", "Ciencia")
enriquecedor.enlazar_entidad(DATA["categoria_gobierno"], "Q7188", "Gobierno")

# Simular datos obtenidos de Wikidata
enriquecedor.agregar_datos_externos(DATA["categoria_tecnologia"], {
    "P279": "Sector económico terciario",
    "P910": "Categoría: Tecnología de la información"
})

print("=== AC-7: Enriquecimiento con Wikidata ===\n")
print(f"Triples totales tras enriquecimiento: {kg.total_triples()}")
print(f"Enlaces externos creados: {len(enriquecedor.enlaces_externos)}")

print("\nEnlaces locales → Wikidata:")
for enlace in enriquecedor.consulta_enriquecimiento():
    local_short = str(enlace.local).split('/')[-1]
    externo_short = str(enlace.externo).split('/')[-1]
    print(f"  {local_short} → {externo_short} ({enlace.etiqueta})")

print("\nQuery sugerida para Wikidata (tecnología):")
print(enriquecedor.generar_query_wikidata('tecnologia'))