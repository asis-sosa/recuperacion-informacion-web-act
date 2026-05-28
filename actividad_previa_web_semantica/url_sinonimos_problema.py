fuente_a = [
    ("París", "esCapitalDe", "Francia"),
    ("París Hilton", "esTipo", "Persona"),
    ("FR", "nombreOficial", "République française"),
]

fuente_b = [
    ("http://geo.example/city/paris", "capital", "http://geo.example/country/fr"),
    ("http://people.example/paris_hilton", "rdf:type", "Person"),
    ("http://geo.example/country/fr", "label", "France"),
]

fuente_c = {
    "wd:Q90": "París (ciudad)",
    "wd:Q47899": "Paris Hilton",
    "wd:Q142": "Francia",
}

uri_labels = {
    "http://geo.example/city/paris": "París (ciudad)",
    "http://people.example/paris_hilton": "Paris Hilton",
    "http://geo.example/country/fr": "Francia",
}

same_as = {
    "París": "http://geo.example/city/paris",
    "Francia": "http://geo.example/country/fr",
    "FR": "http://geo.example/country/fr",
    "París Hilton": "http://people.example/paris_hilton",
}

def resolver(nombre_o_uri):
    return uri_labels.get(
        nombre_o_uri,
        uri_labels.get(same_as.get(nombre_o_uri, ""), nombre_o_uri)
    )

for termino in ["París", "http://geo.example/city/paris", "París Hilton"]:
    print(termino, "->", resolver(termino))