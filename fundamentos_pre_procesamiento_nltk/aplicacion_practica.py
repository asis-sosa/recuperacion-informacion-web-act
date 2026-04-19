from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Carga del conjunto (set) de palabras vacías para el idioma español
vocabulario_stopwords = set(stopwords.words('spanish'))

documento = """
  La arquitectura de computadoras define la estructura y el comportamiento de un sistema informático. 
  Una buena arquitectura optimiza el rendimiento del sistema y minimiza el consumo de energía. 
  El diseño de la estructura del sistema es un desafío constante en la ingeniería de computadoras.
  """

# Pipeline integrado
tokens_doc = word_tokenize(documento, language='spanish')
vector_tokens_procesados = [t.lower() for t in tokens_doc if t.isalpha() and t.lower() not in vocabulario_stopwords]

tokens_originales = len(tokens_doc)
tokens_procesados = len(vector_tokens_procesados)
reduccion = ((tokens_originales - tokens_procesados) / tokens_originales) * 100

# Cálculo de la distribución de frecuencias
distribucion = FreqDist(vector_tokens_procesados)

print("Cantidad de tokens generados:", tokens_originales)
print("Cantidad de tokens procesados: ", tokens_procesados)
print("Vector de características final:", vector_tokens_procesados)
print("Reduccion del: ", reduccion, " %")
print("Términos con mayor frecuencia absoluta (Top 5):")
for termino, frecuencia in distribucion.most_common(5):
    print(f"- {termino}: {frecuencia} apariciones")
