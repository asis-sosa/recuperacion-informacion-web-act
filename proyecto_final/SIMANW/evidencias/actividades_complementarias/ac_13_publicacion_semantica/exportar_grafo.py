from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF

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

print("Exportando grafo...")

kg.graph.serialize(
    destination="simanw_kg.ttl",
    format="turtle"
)

kg.graph.serialize(
    destination="simanw_kg.jsonld",
    format="json-ld"
)

print("Archivos generados:")
print("- simanw_kg.ttl")
print("- simanw_kg.jsonld")