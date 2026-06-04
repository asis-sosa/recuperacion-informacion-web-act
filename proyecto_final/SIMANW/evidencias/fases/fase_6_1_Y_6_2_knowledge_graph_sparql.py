from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "fecha": "2026-05-10",
        "autor": "María García",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.45},
        "url": "https://portal.com/noticias/ia-generativa-2026"
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación.",
        "fecha": "2026-05-09",
        "autor": "Carlos Ruiz",
        "categoria_original": "economia",
        "categoria_predicha": "economia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.35},
        "url": "https://portal.com/noticias/mercados-volatilidad"
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
        "fecha": "2026-05-07",
        "autor": "Juan Hernández",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.38},
        "url": "https://portal.com/noticias/python-314"
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "fecha": "2026-05-06",
        "autor": "Pedro Sánchez",
        "categoria_original": "gobierno",
        "categoria_predicha": "politica",
        "sentimiento": {"etiqueta": "neutral", "compound": 0.0},
        "url": "https://portal.com/noticias/datos-abiertos-gob"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio preocupante sobre el calentamiento global.",
        "fecha": "2026-05-08",
        "autor": "Ana López",
        "categoria_original": "ciencia",
        "categoria_predicha": "ciencia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.42},
        "url": "https://portal.com/noticias/clima-estudio-2026"
    }
]


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

for i, noticia in enumerate(noticias):
    kg.agregar_noticia(noticia, i + 1)


print("=== FASE 6.1: Knowledge Graph ===\n")

print("Knowledge Graph construido:")
print(f"  Total de triples: {kg.total_triples()}")
print(f"  Noticias almacenadas: {len(noticias)}")

print("\nOntología y datos, fragmento en Turtle:")

turtle = kg.serializar("turtle")
lineas = [l for l in turtle.split("\n") if l.strip()][:25]

for linea in lineas:
    print(f"  {linea}")


print("\n=== FASE 6.2: Consultas SPARQL ===\n")

query1 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?titulo ?autor ?categoria ?fecha
WHERE {
    ?noticia a simanw:Noticia ;
             dc:title ?titulo ;
             dc:date ?fecha ;
             simanw:tieneAutor ?autorURI ;
             simanw:tieneCategoria ?catURI .
    ?autorURI foaf:name ?autor .
    ?catURI rdfs:label ?categoria .
}
ORDER BY DESC(?fecha)
"""

print("Consulta 1: Noticias con metadatos")
print("-" * 60)

for row in kg.consultar(query1):
    print(f"[{row.fecha}] [{row.categoria}] {str(row.titulo)[:45]}... - {row.autor}")


query2 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?titulo ?score ?etiqueta
WHERE {
    ?noticia a simanw:Noticia ;
             dc:title ?titulo ;
             simanw:sentimientoScore ?score ;
             simanw:sentimientoEtiqueta ?etiqueta .
    FILTER(?score < -0.05)
}
ORDER BY ?score
"""

print("\nConsulta 2: Noticias con sentimiento negativo")
print("-" * 60)

for row in kg.consultar(query2):
    print(f"[{float(row.score):+.3f}] {str(row.titulo)[:55]}...")


query3 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?categoria (COUNT(?noticia) AS ?total)
WHERE {
    ?noticia a simanw:Noticia ;
             simanw:tieneCategoria ?catURI .
    ?catURI rdfs:label ?categoria .
}
GROUP BY ?categoria
ORDER BY DESC(?total)
"""

print("\nConsulta 3: Distribución por categoría")
print("-" * 60)

for row in kg.consultar(query3):
    print(f"{row.categoria}: {row.total} noticia(s)")


query4 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?autor (COUNT(?n) AS ?publicaciones)
WHERE {
    ?n a simanw:Noticia ;
       dc:title ?titulo ;
       simanw:tieneAutor ?a .
    ?a foaf:name ?autor .
}
GROUP BY ?autor
"""

print("\nConsulta 4: Productividad por autor")
print("-" * 60)

for row in kg.consultar(query4):
    print(f"{row.autor}: {row.publicaciones} publicación(es)")