from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

texto_crudo = "El procesamiento de señales y el análisis de texto comparten principios matemáticos fundamentales."

# Generación de la lista de tokens
tokens = word_tokenize(texto_crudo, language='spanish')

# Plegado de mayúsculas (Case folding)
tokens_normalizados = [token.lower() for token in tokens]

# Filtrado de caracteres especiales y signos de puntuación
# La función .isalpha() evalúa si el string contiene únicamente caracteres alfabéticos
tokens_limpios = [token for token in tokens_normalizados if token.isalpha()]

# Carga del conjunto (set) de palabras vacías para el idioma español
vocabulario_stopwords = set(stopwords.words('spanish'))

# Filtrado mediante exclusión
tokens_con_significado = [token for token in tokens_limpios if token not in vocabulario_stopwords]

print("Longitud de la cadena original:", len(texto_crudo), "caracteres")
print("Cantidad de tokens generados:", len(tokens))
print("Vector de tokens:", tokens)
print("Tokens tras normalización y filtrado:", tokens_limpios)
print("Vector de características final:", tokens_con_significado)
