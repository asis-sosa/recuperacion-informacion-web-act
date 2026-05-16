corpus_mision1 = {
    "d1": "La red de agentes interceptó tráfico sospechoso en el nodo norte.",
    "d2": "El agente de campo reportó actividad normal en la red interna.",
    "d3": "Manual de procedimientos: la red no debe apagarse sin autorización.",
    "d4": "Mantenimiento programado del agente automático de respaldo.",
}

# 1. Tokenización y creación del índice invertido

indice_invertido = {}

# Recorrer cada documento del corpus
for doc_id, texto in corpus_mision1.items():

    texto = texto.lower()

    texto = texto.replace(".", "")
    texto = texto.replace(",", "")
    texto = texto.replace(":", "")

    # Tokenizar
    tokens = texto.split()

    for token in tokens:
        # Si el término no existe en el índice, crearlo
        if token not in indice_invertido:
            indice_invertido[token] = []

        # Evitar documentos repetidos
        if doc_id not in indice_invertido[token]:
            indice_invertido[token].append(doc_id)

print("ÍNDICE INVERTIDO:\n")

for termino, documentos in sorted(indice_invertido.items()):
    print(f"{termino} -> {documentos}")

# 2. Consulta booleana: "agente" AND "red"

termino1 = "agente"
termino2 = "red"

# Obtener listas de documentos
docs_termino1 = set(indice_invertido.get(termino1, []))
docs_termino2 = set(indice_invertido.get(termino2, []))

# Operación AND (intersección)
resultado = sorted(docs_termino1.intersection(docs_termino2))

# 3. Mostrar resultados

print("\nRESULTADO DE LA CONSULTA:")
print(f'"{termino1}" AND "{termino2}"')

print("\nDocumentos coincidentes:")
print(resultado)