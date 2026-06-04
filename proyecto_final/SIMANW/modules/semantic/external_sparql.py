try:
    from SPARQLWrapper import SPARQLWrapper, JSON
except ImportError:
    SPARQLWrapper = None
    JSON = None


QUERY_WIKIDATA = """
SELECT ?item ?itemLabel ?description WHERE {
  ?item wdt:P31 wd:Q7397;
        wdt:P277 wd:Q28865;
        wdt:P366 wd:Q11660.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
}
LIMIT 10
"""

QUERY_DBPEDIA = """
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


def consultas_documentadas():
    return {
        "wikidata": {
            "endpoint": "https://query.wikidata.org/sparql",
            "descripcion": "Consulta de software relacionado con inteligencia artificial y Python.",
            "query": QUERY_WIKIDATA
        },
        "dbpedia": {
            "endpoint": "http://dbpedia.org/sparql",
            "descripcion": "Consulta de recursos relacionados con procesamiento de lenguaje natural.",
            "query": QUERY_DBPEDIA
        }
    }


def ejecutar_consulta_wikidata():
    if SPARQLWrapper is None:
        return {
            "ok": False,
            "error": "SPARQLWrapper no está instalado. Ejecuta: pip install SPARQLWrapper"
        }

    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(QUERY_WIKIDATA)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        filas = []

        for r in results["results"]["bindings"]:
            filas.append({
                "item": r.get("item", {}).get("value", ""),
                "label": r.get("itemLabel", {}).get("value", ""),
                "description": r.get("description", {}).get("value", "")
            })

        return {
            "ok": True,
            "resultados": filas
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }