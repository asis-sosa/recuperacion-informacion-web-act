from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF, SKOS
from pathlib import Path


class KnowledgeGraphSIMANW:
    def __init__(self):
        self.graph = Graph()

        self.NS = Namespace("http://simanw.org/ontology/")
        self.DATA = Namespace("http://simanw.org/data/")
        self.WD = Namespace("http://www.wikidata.org/entity/")

        self.graph.bind("simanw", self.NS)
        self.graph.bind("data", self.DATA)
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)
        self.graph.bind("skos", SKOS)
        self.graph.bind("wd", self.WD)

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

        self.graph.add((self.NS.relacionadaConDataset, RDF.type, OWL.ObjectProperty))

    def agregar_noticia(self, noticia, noticia_id):
        uri = self.DATA[f"noticia_{noticia_id}"]

        self.graph.add((uri, RDF.type, self.NS.Noticia))
        self.graph.add((uri, DC.title, Literal(noticia["titulo"], lang="es")))
        self.graph.add((uri, DC.description, Literal(noticia["cuerpo"], lang="es")))
        self.graph.add((uri, DC.date, Literal(noticia.get("fecha", ""), datatype=XSD.date)))

        autor = noticia.get("autor", "Desconocido")
        autor_uri = self.DATA[f"autor_{autor.replace(' ', '_')}"]

        self.graph.add((autor_uri, RDF.type, self.NS.Autor))
        self.graph.add((autor_uri, FOAF.name, Literal(autor)))
        self.graph.add((uri, self.NS.tieneAutor, autor_uri))

        categoria = noticia.get("categoria_predicha", noticia.get("categoria_original", "general"))
        cat_uri = self.DATA[f"categoria_{categoria}"]

        self.graph.add((cat_uri, RDF.type, self.NS.Categoria))
        self.graph.add((cat_uri, RDFS.label, Literal(categoria, lang="es")))
        self.graph.add((uri, self.NS.tieneCategoria, cat_uri))

        sentimiento = noticia.get("sentimiento", {})

        if sentimiento:
            self.graph.add((
                uri,
                self.NS.sentimientoScore,
                Literal(sentimiento.get("compound", 0), datatype=XSD.float)
            ))

            self.graph.add((
                uri,
                self.NS.sentimientoEtiqueta,
                Literal(sentimiento.get("etiqueta", "neutral"))
            ))

        if noticia.get("url"):
            self.graph.add((
                uri,
                self.NS.urlOriginal,
                Literal(noticia["url"], datatype=XSD.anyURI)
            ))

    def enriquecer_categorias(self):
        enlaces = {
            "tecnologia": ("Q11016", "Tecnología de la información"),
            "economia": ("Q159810", "Economía"),
            "ciencia": ("Q336", "Ciencia"),
            "politica": ("Q7188", "Gobierno"),
            "gobierno": ("Q7188", "Gobierno"),
            "salud": ("Q12136", "Enfermedad"),
            "videojuegos": ("Q7889", "Videojuego")
        }

        for categoria, (wikidata_id, etiqueta) in enlaces.items():
            cat_uri = self.DATA[f"categoria_{categoria}"]

            self.graph.add((cat_uri, OWL.sameAs, self.WD[wikidata_id]))
            self.graph.add((cat_uri, SKOS.exactMatch, self.WD[wikidata_id]))
            self.graph.add((self.WD[wikidata_id], RDFS.label, Literal(etiqueta, lang="es")))

    def construir_desde_noticias(self, noticias):
        for i, noticia in enumerate(noticias, 1):
            self.agregar_noticia(noticia, i)

        self.enriquecer_categorias()

    def consultar(self, query):
        return list(self.graph.query(query))

    def total_triples(self):
        return len(self.graph)

    def exportar(self):
        Path("data/rdf").mkdir(parents=True, exist_ok=True)

        self.graph.serialize(
            destination="data/rdf/simanw_kg.ttl",
            format="turtle"
        )

        self.graph.serialize(
            destination="data/rdf/simanw_kg.jsonld",
            format="json-ld"
        )

    def consultas_demo(self):
        consulta_categorias = """
        PREFIX simanw: <http://simanw.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?categoria (COUNT(?noticia) AS ?total)
        WHERE {
            ?noticia a simanw:Noticia ;
                     simanw:tieneCategoria ?cat .
            ?cat rdfs:label ?categoria .
        }
        GROUP BY ?categoria
        ORDER BY DESC(?total)
        """

        consulta_negativas = """
        PREFIX simanw: <http://simanw.org/ontology/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        SELECT ?titulo ?score
        WHERE {
            ?noticia a simanw:Noticia ;
                     dc:title ?titulo ;
                     simanw:sentimientoScore ?score .
            FILTER(?score < -0.05)
        }
        ORDER BY ?score
        """

        consulta_enlaces = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?local ?externo ?etiqueta
        WHERE {
            ?local owl:sameAs ?externo .
            ?externo rdfs:label ?etiqueta .
        }
        """

        return {
            "categorias": self.consultar(consulta_categorias),
            "sentimiento_negativo": self.consultar(consulta_negativas),
            "enlaces_externos": self.consultar(consulta_enlaces)
        }

    def agregar_noticia_incompleta_prueba(self):
        uri = self.DATA["noticia_prueba_incompleta"]

        self.graph.add((uri, RDF.type, self.NS.Noticia))

        # Intencionalmente solo agregamos fecha.
        # No agregamos dc:title, dc:description, autor ni categoría.
        self.graph.add((uri, DC.date, Literal("2026-10-01", datatype=XSD.date)))