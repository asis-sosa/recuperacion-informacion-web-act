from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "fecha": "2026-05-10",
        "autor": "María García",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.45},
        "url": "https://portal.com/noticias/ia-generativa-2026"
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación.",
        "fecha": "2026-05-09",
        "autor": "Carlos Ruiz",
        "categoria_predicha": "economia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.35},
        "url": "https://portal.com/noticias/mercados-volatilidad"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio sobre el calentamiento global.",
        "fecha": "2026-05-08",
        "autor": "Ana López",
        "categoria_predicha": "ciencia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.42},
        "url": "https://portal.com/noticias/clima-estudio-2026"
    },
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

        self.graph.add((self.NS.tieneAutor, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.tieneCategoria, RDF.type, OWL.ObjectProperty))

        self.graph.add((self.NS.sentimientoScore, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.sentimientoEtiqueta, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.urlOriginal, RDF.type, OWL.DatatypeProperty))

    def agregar_noticia(self, noticia, noticia_id):
        uri = self.DATA[f"noticia_{noticia_id}"]

        self.graph.add((uri, RDF.type, self.NS.Noticia))
        self.graph.add((uri, DC.title, Literal(noticia["titulo"], lang="es")))
        self.graph.add((uri, DC.description, Literal(noticia["cuerpo"], lang="es")))
        self.graph.add((uri, DC.date, Literal(noticia["fecha"], datatype=XSD.date)))

        autor_uri = self.DATA[f"autor_{noticia['autor'].replace(' ', '_')}"]
        self.graph.add((autor_uri, RDF.type, self.NS.Autor))
        self.graph.add((autor_uri, FOAF.name, Literal(noticia["autor"])))
        self.graph.add((uri, self.NS.tieneAutor, autor_uri))

        categoria = noticia["categoria_predicha"]
        cat_uri = self.DATA[f"categoria_{categoria}"]

        self.graph.add((cat_uri, RDF.type, self.NS.Categoria))
        self.graph.add((cat_uri, RDFS.label, Literal(categoria, lang="es")))
        self.graph.add((uri, self.NS.tieneCategoria, cat_uri))

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

        self.graph.add((
            uri,
            self.NS.urlOriginal,
            Literal(noticia["url"], datatype=XSD.anyURI)
        ))

    def total_triples(self):
        return len(self.graph)


class ConectorDatosAbiertos:
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph

        self.DCAT = Namespace("http://www.w3.org/ns/dcat#")
        self.GOB = Namespace("http://datos.gob.mx/")

        self.kg.graph.bind("dcat", self.DCAT)
        self.kg.graph.bind("gob", self.GOB)

    def cargar_dataset_gobierno(self, nombre, datos, publicador, tema):
        ds_uri = self.GOB[f"dataset/{nombre.replace(' ', '_')}"]

        self.kg.graph.add((ds_uri, RDF.type, self.DCAT.Dataset))
        self.kg.graph.add((ds_uri, DC.title, Literal(nombre, lang="es")))
        self.kg.graph.add((ds_uri, DC.publisher, Literal(publicador)))
        self.kg.graph.add((ds_uri, self.GOB.tema, Literal(tema)))

        for i, registro in enumerate(datos):
            reg_uri = self.GOB[f"registro/{nombre.replace(' ', '_')}_{i}"]
            self.kg.graph.add((ds_uri, self.GOB.tieneRegistro, reg_uri))

            for campo, valor in registro.items():
                if isinstance(valor, (int, float)):
                    self.kg.graph.add((
                        reg_uri,
                        self.GOB[campo],
                        Literal(valor, datatype=XSD.float)
                    ))
                else:
                    self.kg.graph.add((
                        reg_uri,
                        self.GOB[campo],
                        Literal(valor, lang="es")
                    ))

    def consultar_datos(self, tema=None):
        filtro = f'FILTER(?tema = "{tema}")' if tema else ""

        query = f"""
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX gob: <http://datos.gob.mx/>

        SELECT ?titulo ?publicador ?tema
        WHERE {{
            ?ds a dcat:Dataset ;
                dc:title ?titulo ;
                dc:publisher ?publicador ;
                gob:tema ?tema .
            {filtro}
        }}
        """

        return list(self.kg.graph.query(query))

    def enlazar_noticias_con_datos(self):
        query = """
        PREFIX simanw: <http://simanw.org/ontology/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX gob: <http://datos.gob.mx/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?noticia_titulo ?dataset_titulo ?tema
        WHERE {
            ?noticia a simanw:Noticia ;
                     dc:title ?noticia_titulo ;
                     simanw:tieneCategoria ?cat .
            ?cat rdfs:label ?cat_label .

            ?ds a dcat:Dataset ;
                dc:title ?dataset_titulo ;
                gob:tema ?tema .

            FILTER(CONTAINS(LCASE(?tema), LCASE(?cat_label)))
        }
        """

        return list(self.kg.graph.query(query))


kg = KnowledgeGraphSIMANW()

for i, noticia in enumerate(noticias):
    kg.agregar_noticia(noticia, i + 1)


conector = ConectorDatosAbiertos(kg)

conector.cargar_dataset_gobierno(
    "Presupuesto TIC Federal 2026",
    [
        {
            "dependencia": "SEP",
            "monto_mdp": 12500,
            "concepto": "Infraestructura digital educativa"
        },
        {
            "dependencia": "SALUD",
            "monto_mdp": 8900,
            "concepto": "Expediente clínico electrónico"
        },
        {
            "dependencia": "SAT",
            "monto_mdp": 15600,
            "concepto": "Plataformas de recaudación"
        },
    ],
    publicador="Secretaría de Hacienda",
    tema="tecnologia"
)

conector.cargar_dataset_gobierno(
    "Indicadores Económicos Mayo 2026",
    [
        {
            "indicador": "Inflación anual",
            "valor": 4.2,
            "unidad": "porcentaje"
        },
        {
            "indicador": "Tipo de cambio",
            "valor": 18.5,
            "unidad": "pesos por dólar"
        },
        {
            "indicador": "Tasa de desempleo",
            "valor": 3.1,
            "unidad": "porcentaje"
        },
    ],
    publicador="INEGI / Banco de México",
    tema="economia"
)

conector.cargar_dataset_gobierno(
    "Emisiones CO2 por Sector 2025",
    [
        {
            "sector": "Energía",
            "emisiones_mtco2": 450,
            "variacion": -2.1
        },
        {
            "sector": "Transporte",
            "emisiones_mtco2": 180,
            "variacion": 1.5
        },
        {
            "sector": "Industria",
            "emisiones_mtco2": 120,
            "variacion": -3.8
        },
    ],
    publicador="SEMARNAT",
    tema="ciencia"
)


print("=== FASE 6.3: Datos Abiertos Integrados ===\n")

print(f"Triples totales en KG con datos abiertos: {kg.total_triples()}")

print("\nDatasets de datos abiertos cargados:")

for row in conector.consultar_datos():
    print(f"[{row.tema}] {row.titulo} - {row.publicador}")

print("\nEnlaces noticias ↔ datos abiertos:")

enlaces = conector.enlazar_noticias_con_datos()

if enlaces:
    for row in enlaces:
        print(f"Noticia: {str(row.noticia_titulo)[:50]}...")
        print(f"Dataset: {row.dataset_titulo}")
        print(f"Tema: {row.tema}")
        print()
else:
    print("(Los enlaces se generan cuando las categorías coinciden con los temas)")


print("\n=== FASE 6.4: Endpoints SPARQL Externos ===\n")

query_wikidata = """
SELECT ?item ?itemLabel ?description WHERE {
  ?item wdt:P31 wd:Q7397;
        wdt:P277 wd:Q28865;
        wdt:P366 wd:Q11660.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
}
LIMIT 10
"""

query_dbpedia = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?nombre ?descripcion WHERE {
  ?s dbo:genre dbr:Natural_language_processing ;
     rdfs:label ?nombre ;
     rdfs:comment ?descripcion .
  FILTER(LANG(?nombre) = 'es')
  FILTER(LANG(?descripcion) = 'es')
}
LIMIT 5
"""

print("Consulta para Wikidata:")
print(query_wikidata)

print("\nConsulta para DBpedia:")
print(query_dbpedia)

print("""
Endpoints SPARQL disponibles para el SIMANW:
- Wikidata: https://query.wikidata.org/sparql
- DBpedia: http://dbpedia.org/sparql
- datos.gob: Portal de datos abiertos de México

Código de ejecución real, requiere internet:

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(query_wikidata)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
""")