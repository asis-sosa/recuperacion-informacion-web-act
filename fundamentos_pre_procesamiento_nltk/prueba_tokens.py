from nltk.tokenize import word_tokenize

texto_crudo = "El procesamiento de señales y el análisis de texto comparten principios matemáticos fundamentales."

# Generación de la lista de tokens
tokens = word_tokenize(texto_crudo, language='spanish')

print("Longitud de la cadena original:", len(texto_crudo), "caracteres")
print("Cantidad de tokens generados:", len(tokens))
print("Vector de tokens:", tokens)
