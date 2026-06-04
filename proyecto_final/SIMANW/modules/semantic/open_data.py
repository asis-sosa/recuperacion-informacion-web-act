from rdflib import Namespace, Literal, RDF, XSD
from rdflib.namespace import DC


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

    def cargar_datasets_demo(self):
        self.cargar_dataset_gobierno(
            "Presupuesto TIC Federal 2026",
            [
                {"dependencia": "SEP", "monto_mdp": 12500, "concepto": "Infraestructura digital educativa"},
                {"dependencia": "SALUD", "monto_mdp": 8900, "concepto": "Expediente clínico electrónico"},
                {"dependencia": "SAT", "monto_mdp": 15600, "concepto": "Plataformas de recaudación"},
            ],
            publicador="Secretaría de Hacienda",
            tema="tecnologia"
        )

        self.cargar_dataset_gobierno(
            "Indicadores Económicos Mayo 2026",
            [
                {"indicador": "Inflación anual", "valor": 4.2, "unidad": "porcentaje"},
                {"indicador": "Tipo de cambio", "valor": 18.5, "unidad": "pesos por dólar"},
                {"indicador": "Tasa de desempleo", "valor": 3.1, "unidad": "porcentaje"},
            ],
            publicador="INEGI / Banco de México",
            tema="economia"
        )

        self.cargar_dataset_gobierno(
            "Emisiones CO2 por Sector 2025",
            [
                {"sector": "Energía", "emisiones_mtco2": 450, "variacion": -2.1},
                {"sector": "Transporte", "emisiones_mtco2": 180, "variacion": 1.5},
                {"sector": "Industria", "emisiones_mtco2": 120, "variacion": -3.8},
            ],
            publicador="SEMARNAT",
            tema="ciencia"
        )

        self.cargar_dataset_gobierno(
            "Indicadores de Salud Digital 2026",
            [
                {"indicador": "Expedientes digitales", "valor": 72, "unidad": "porcentaje"},
                {"indicador": "Teleconsultas", "valor": 18500, "unidad": "consultas"},
                {"indicador": "Hospitales conectados", "valor": 310, "unidad": "hospitales"},
            ],
            publicador="Secretaría de Salud",
            tema="salud"
        )

        self.cargar_dataset_gobierno(
            "Economía de Videojuegos 2026",
            [
                {"indicador": "Ingresos gaming", "valor": 2400, "unidad": "millones de pesos"},
                {"indicador": "Eventos eSports", "valor": 42, "unidad": "eventos"},
                {"indicador": "Usuarios activos", "valor": 18.7, "unidad": "millones"},
            ],
            publicador="Observatorio Digital",
            tema="videojuegos"
        )

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
    
        SELECT ?noticia_titulo ?dataset_titulo
        WHERE {
            ?noticia simanw:relacionadaConDataset ?dataset ;
                     dc:title ?noticia_titulo .
    
            ?dataset dc:title ?dataset_titulo .
        }
        """
    
        return list(self.kg.graph.query(query))

    def crear_enlaces_semanticos(self):
        query = """
        PREFIX simanw: <http://simanw.org/ontology/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX gob: <http://datos.gob.mx/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?noticia ?noticia_titulo ?dataset ?dataset_titulo ?cat_label ?tema
        WHERE {
            ?noticia a simanw:Noticia ;
                     dc:title ?noticia_titulo ;
                     simanw:tieneCategoria ?cat .

            ?cat rdfs:label ?cat_label .

            ?dataset a dcat:Dataset ;
                     dc:title ?dataset_titulo ;
                     gob:tema ?tema .
        }
        """

        resultados = list(self.kg.graph.query(query))
        enlaces_creados = []

        for row in resultados:
            cat = str(row.cat_label).lower().strip()
            tema = str(row.tema).lower().strip()

            if cat == tema or cat in tema or tema in cat:
                self.kg.graph.add((
                    row.noticia,
                    self.kg.NS.relacionadaConDataset,
                    row.dataset
                ))

                enlaces_creados.append({
                    "noticia": str(row.noticia_titulo),
                    "dataset": str(row.dataset_titulo),
                    "tema": tema
                })

        return enlaces_creados