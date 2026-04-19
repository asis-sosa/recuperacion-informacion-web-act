# **FUNDAMENTOS Y PRE-PROCESAMIENTO EN NLTK**

## Objetivo

Introducir a los estudiantes en la configuración de entornos para análisis de datos y en el pipeline estándar de pre-procesamiento de texto utilizando la biblioteca NLTK (Natural Language Toolkit) en Python. Al finalizar la práctica, el alumno será capaz de transformar texto no estructurado en una representación analizable basada en la frecuencia de términos.

## Fase 1: Configuración del Entorno de Desarrollo e Instalación

Como buena práctica en el desarrollo de software y ciencia de datos, el primer paso es aislar las dependencias del proyecto utilizando un entorno virtual. Esto evita conflictos con otras bibliotecas instaladas a nivel global en el sistema operativo.

**Instrucción:** Abra su terminal o línea de comandos y ejecute la siguiente secuencia para crear el entorno, activarlo e instalar la biblioteca requerida.

  ┌────
  │ # 1. Crear un entorno virtual llamado 'nlp_env'
  │ python -m venv nlp_env
  │ 
  │ # 2. Activar el entorno virtual
  │ # En Windows:
  │ nlp_env\Scripts\activate
  │ # En macOS/Linux:
  │ source nlp_env/bin/activate
  │ 
  │ # 3. Instalar la biblioteca NLTK mediante el gestor de paquetes pip
  │ pip install nltk
  └────

## Fase 2: Inicialización de Recursos Léxicos (Corpus)

El análisis computacional del lenguaje requiere modelos pre-entrenados y vocabularios específicos del idioma. NLTK maneja estos recursos de manera modular, por lo que no se descargan automáticamente con la biblioteca para ahorrar espacio; debemos solicitarlos explícitamente.

**Instrucción:** Cree un nuevo archivo de Python (ej. `laboratorio_nlp.py') y ejecute el siguiente bloque para descargar los corpus necesarios para la práctica de hoy. (comando desde la terminal -> python -m idlelib document_name.py)

  ┌────
  │ import nltk
  │ 
  │ # Descarga del tokenizador 'punkt' (modelo para segmentar oraciones y palabras)
  │ nltk.download('punkt')
  │ 
  │ # Descarga del corpus de palabras de paro (stopwords)
  │ nltk.download('stopwords')
  │ 
  │ print("Recursos léxicos descargados y entorno configurado correctamente.")
  └────

## Fase 3: Segmentación Léxica (Tokenización)

La tokenización es el proceso de convertir una cadena de caracteres continua (string) en una secuencia de componentes discretos o unidades léxicas (tokens).

**Instrucción:** Analice el siguiente código. Observe cómo la función `word_tokenize' identifica los límites de las palabras basándose en la gramática del idioma especificado.

  ┌────
  │ from nltk.tokenize import word_tokenize
  │ 
  │ texto_crudo = "El procesamiento de señales y el análisis de texto comparten principios matemáticos fundamentales."
  │ 
  │ # Generación de la lista de tokens
  │ tokens = word_tokenize(texto_crudo, language='spanish')
  │ 
  │ print("Longitud de la cadena original:", len(texto_crudo), "caracteres")
  │ print("Cantidad de tokens generados:", len(tokens))
  │ print("Vector de tokens:", tokens)
  └────

**Resultados**

>- print("Longitud de la cadena original:", len(texto_crudo), "caracteres")
>- Longitud de la cadena original: 98 caracteres

>- print("Cantidad de tokens generados:", len(tokens))
>- Cantidad de tokens generados: 14

>- print("Vector de tokens:", tokens)
>- Vector de tokens: ['El', 'procesamiento', 'de', 'señales', 'y', 'el', 'análisis', 'de', 'texto', 'comparten', 'principios', 'matemáticos', 'fundamentales', '.']

## Fase 4: Normalización y Filtrado Alfanumérico

Para un sistema computacional, las variaciones en mayúsculas/minúsculas y los signos de puntuación incrementan artificialmente la dimensionalidad del vocabulario (ej. "Sistema" y "sistema" se evaluarían como entidades distintas). La normalización estandariza el espacio de entrada.

**Instrucción:** Aplique técnicas de comprensión de listas en Python para estandarizar el corpus.

  ┌────
  │ # 1. Plegado de mayúsculas (Case folding)
  │ tokens_normalizados = [token.lower() for token in tokens]
  │ 
  │ # 2. Filtrado de caracteres especiales y signos de puntuación
  │ # La función .isalpha() evalúa si el string contiene únicamente caracteres alfabéticos
  │ tokens_limpios = [token for token in tokens_normalizados if token.isalpha()]
  │ 
  │ print("Tokens tras normalización y filtrado:", tokens_limpios)
  └────

**Resultado**

>- print("Vector de tokens:", tokens)
>- Vector de tokens: ['El', 'procesamiento', 'de', 'señales', 'y', 'el', 'análisis', 'de', 'texto', 'comparten', 'principios', 'matemáticos', 'fundamentales', '.']

>- print("Tokens tras normalización y filtrado:", tokens_limpios)
>- Tokens tras normalización y filtrado: ['el', 'procesamiento', 'de', 'señales', 'y', 'el', 'análisis', 'de', 'texto', 'comparten', 'principios', 'matemáticos', 'fundamentales']

## Fase 5: Eliminación de Palabras Vacías (Stopwords)

Los artículos, preposiciones y conjunciones poseen una alta frecuencia de aparición, pero aportan una cantidad marginal de ganancia de
información (Information Gain) respecto a la semántica del documento. Su eliminación reduce la carga computacional y mejora la señal de los términos relevantes.

**Instrucción:** Utilice el corpus de NLTK descargado en la Fase 2 para filtrar estas palabras.

  ┌────
  │ from nltk.corpus import stopwords
  │ 
  │ # Carga del conjunto (set) de palabras vacías para el idioma español
  │ vocabulario_stopwords = set(stopwords.words('spanish'))
  │ 
  │ # Filtrado mediante exclusión
  │ tokens_con_significado = [token for token in tokens_limpios if token not in vocabulario_stopwords]
  │ 
  │ print("Vector de características final:", tokens_con_significado)
  └────

**Resultado**

>- print("Tokens tras normalización y filtrado:", tokens_limpios)
>- Tokens tras normalización y filtrado: ['el', 'procesamiento', 'de', 'señales', 'y', 'el', 'análisis', 'de', 'texto', 'comparten', 'principios', 'matemáticos', 'fundamentales']

>- print("Vector de características final:", tokens_con_significado)
>- Vector de características final: ['procesamiento', 'señales', 'análisis', 'texto', 'comparten', 'principios', 'matemáticos', 'fundamentales']

## Fase 6: Análisis de Distribución de Frecuencias

Una vez que el ruido lingüístico ha sido mitigado, es posible cuantificar la relevancia de los términos restantes mediante su frecuencia absoluta.

**Instrucción:** Procesaremos un texto de mayor longitud aplicando el pipeline completo desarrollado en las fases anteriores, para finalmente obtener su distribución de frecuencias.

  ┌────
  │ from nltk.probability import FreqDist
  │ 
  │ documento = """
  │ La arquitectura de computadoras define la estructura y el comportamiento de un sistema informático. 
  │ Una buena arquitectura optimiza el rendimiento del sistema y minimiza el consumo de energía. 
  │ El diseño de la estructura del sistema es un desafío constante en la ingeniería de computadoras.
  │ """
  │ 
  │ # Pipeline integrado
  │ tokens_doc = word_tokenize(documento, language='spanish')
  │ tokens_procesados = [t.lower() for t in tokens_doc if t.isalpha() and t.lower() not in vocabulario_stopwords]
  │ 
  │ # Cálculo de la distribución de frecuencias
  │ distribucion = FreqDist(tokens_procesados)
  │ 
  │ print("Términos con mayor frecuencia absoluta (Top 3):")
  │ for termino, frecuencia in distribucion.most_common(3):
  │     print(f"- {termino}: {frecuencia} apariciones")
  └────

**Resultado**

>- print("Términos con mayor frecuencia absoluta (Top 3):")
for termino, frecuencia in distribucion.most_common(3):
    print(f"- {termino}: {frecuencia} apariciones")

>- Términos con mayor frecuencia absoluta (Top 3):
>- - sistema: 3 apariciones
>- - arquitectura: 2 apariciones
>- - computadoras: 2 apariciones

## Ejercicio de Aplicación Práctica

1. Seleccione un resumen (/abstract/) de un artículo científico
     relacionado con su área de estudio (mínimo 100 palabras).
2. Desarrolle un script en Python que implemente el pipeline analizado
     en esta práctica. 
3. El script debe generar como salida estándar (stdout):
- - El número total de tokens originales.
- - El número total de tokens tras el pre-procesamiento.
- - El porcentaje de reducción de dimensionalidad del texto.
- - Los 5 términos más frecuentes.