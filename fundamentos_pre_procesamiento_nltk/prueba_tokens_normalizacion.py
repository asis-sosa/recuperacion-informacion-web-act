from nltk.tokenize import word_tokenize

texto_crudo = "El procesamiento de señales y el análisis de texto comparten principios matemáticos fundamentales."

# Generación de la lista de tokens
tokens = word_tokenize(texto_crudo, language='spanish')

# 1. Plegado de mayúsculas (Case folding)
tokens_normalizados = [token.lower() for token in tokens]

# 2. Filtrado de caracteres especiales y signos de puntuación
# La función .isalpha() evalúa si el string contiene únicamente caracteres alfabéticos
tokens_limpios = [token for token in tokens_normalizados if token.isalpha()]

print("Longitud de la cadena original:", len(texto_crudo), "caracteres")
print("Cantidad de tokens generados:", len(tokens))
print("Vector de tokens:", tokens)
print("Tokens tras normalización y filtrado:", tokens_limpios)
