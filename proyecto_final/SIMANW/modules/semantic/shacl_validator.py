from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DC


class ValidadorSHACL:
    def __init__(self, ttl_path):
        self.ttl_path = ttl_path

        self.SIMANW = Namespace("http://simanw.org/ontology/")

    def validar(self):
        g = Graph()
        g.parse(self.ttl_path, format="turtle")

        noticias = list(g.subjects(RDF.type, self.SIMANW.Noticia))

        violaciones = []

        for noticia in noticias:
            titulo = list(g.objects(noticia, DC.title))
            descripcion = list(g.objects(noticia, DC.description))
            fecha = list(g.objects(noticia, DC.date))
            categoria = list(g.objects(noticia, self.SIMANW.tieneCategoria))
            autor = list(g.objects(noticia, self.SIMANW.tieneAutor))

            if not titulo:
                violaciones.append({
                    "recurso": str(noticia),
                    "problema": "La noticia no tiene dc:title"
                })

            if not descripcion:
                violaciones.append({
                    "recurso": str(noticia),
                    "problema": "La noticia no tiene dc:description"
                })

            if not fecha:
                violaciones.append({
                    "recurso": str(noticia),
                    "problema": "La noticia no tiene dc:date"
                })

            if not categoria:
                violaciones.append({
                    "recurso": str(noticia),
                    "problema": "La noticia no tiene simanw:tieneCategoria"
                })

            if not autor:
                violaciones.append({
                    "recurso": str(noticia),
                    "problema": "La noticia no tiene simanw:tieneAutor"
                })

        return {
            "noticias_validadas": len(noticias),
            "violaciones": violaciones,
            "total_violaciones": len(violaciones)
        }