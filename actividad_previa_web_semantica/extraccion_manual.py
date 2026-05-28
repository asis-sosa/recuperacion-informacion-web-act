html_informe = """
<article id="persona-alicia">
  <h1>Alicia García</h1>
  <p class="rol">Profesora de Matemáticas en la UNAM</p>
  <p>Conoce a <a href="/personas/bob">Bob Martínez</a>, coautor del artículo
     <cite>Redes y Grafos</cite>.</p>
</article>
"""

json_biblioteca = {
    "libro_id": "L-42",
    "titulo": "Introducción a la Web Semántica",
    "autores": ["Alicia García", "Bob Martínez"],
    "anio": 2019,
    "isbn": "978-3-030-00000-0",
}

triples_html = [
    ("ex:alicia", "tieneNombre", "Alicia García"),
    ("ex:alicia", "tieneRol", "Profesora de Matemáticas"),
    ("ex:alicia", "trabajaEn", "UNAM"),
    ("ex:bob", "tieneNombre", "Bob Martínez"),
    ("ex:alicia", "coautorDe", "ex:redes_grafos"),
    ("ex:bob", "coautorDe", "ex:redes_grafos"),
]

triples_json = [
    ("ex:libro_L42", "titulo", "Introducción a la Web Semántica"),
    ("ex:libro_L42", "tieneAutor", "ex:alicia_json"),
    ("ex:libro_L42", "tieneAutor", "ex:bob_json"),
    ("ex:alicia_json", "tieneNombre", "Alicia García"),
]

def cubre(triples, predicados_esperados):
    preds = {p for _, p, _ in triples}
    faltan = set(predicados_esperados) - preds
    print("Predicados presentes:", sorted(preds))
    print("Faltan:", sorted(faltan) if faltan else "ninguno")

cubre(triples_html, {"tieneNombre", "tieneRol", "conoce", "coautorDe"})
cubre(triples_json, {"titulo", "tieneAutor", "publicadoEn"})