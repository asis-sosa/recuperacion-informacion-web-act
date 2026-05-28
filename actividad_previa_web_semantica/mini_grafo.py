G = [
    {"s": "ex:alicia", "p": "tipo", "o": "ex:Persona"},
    {"s": "ex:alicia", "p": "nombre", "o": "Alicia García"},
    {"s": "ex:alicia", "p": "conoce", "o": "ex:bob"},
    {"s": "ex:bob", "p": "nombre", "o": "Bob Martínez"},
    {"s": "ex:bob", "p": "tipo", "o": "ex:Persona"},
    {"s": "ex:libro42", "p": "titulo", "o": "Introducción a la Web Semántica"},
    {"s": "ex:libro42", "p": "autor", "o": "ex:alicia"},
    {"s": "ex:libro42", "p": "autor", "o": "ex:bob"},
    {"s": "ex:libro42", "p": "anio", "o": "2019"},
]

def consulta_simple(g, patron):
    resultados = []
    for t in g:
        asignacion = {}
        ok = True
        for rol in ("s", "p", "o"):
            esperado = patron.get(rol)
            if esperado is None:
                continue
            if t[rol] != esperado:
                ok = False
                break
        if not ok:
            continue
        for rol in ("s", "p", "o"):
            if patron.get(rol) is None:
                asignacion[rol] = t[rol]
        if asignacion and asignacion not in resultados:
            resultados.append(asignacion)
    return resultados


# TAREA A: ¿Quiénes son autores del libro42?
patron_a = {"s": "ex:libro42", "p": "autor", "o": None}
print("Autores:", consulta_simple(G, patron_a))


# TAREA B: patrón para obtener personas
patron_b = {"s": None, "p": "tipo", "o": "ex:Persona"}
print("Personas:", consulta_simple(G, patron_b))


# TAREA C: triple inferido manualmente
G.append({
    "s": "ex:alicia",
    "p": "tieneConocidoPersona",
    "o": "ex:bob"
})

print("Grafo:")
for triple in G:
    print(triple)