# SIMANW

## Sistema Inteligente de Monitoreo y Análisis de Noticias Web

SIMANW es una plataforma desarrollada para la materia de Recuperación de Información Web. El sistema integra técnicas de rastreo web, procesamiento de lenguaje natural, clasificación automática, motores de búsqueda, chatbots, grafos de conocimiento y Web Semántica para analizar noticias de forma automática.

---

# Estructura del proyecto

## app.py

Punto de entrada principal del sistema.

Contiene la interfaz visual desarrollada con Streamlit y permite acceder a todas las funcionalidades del proyecto:

* Inicio
* Buscador Inteligente
* Tendencias
* Chatbot
* Alertas
* Knowledge Graph
* Reportes

---

## assets/

Contiene recursos visuales utilizados por la interfaz.

Ejemplos:

* Hojas de estilo CSS
* Imágenes
* Logotipos
* Recursos gráficos

---

## data/

Almacena los datos procesados por el sistema.

### data/raw/

Contiene noticias obtenidas directamente del rastreo.

Ejemplos:

* noticias_raw.json

### data/processed/

Contiene los datos ya procesados por el pipeline NLP.

Ejemplos:

* noticias_limpias.json
* noticias_procesadas.json
* noticias_analizadas.json

### data/rdf/

Contiene el Knowledge Graph exportado.

Ejemplos:

* simanw_kg.ttl
* simanw_kg.jsonld

---

## modules/

Contiene la lógica principal del sistema.

### modules/crawler/

Implementa los rastreadores web.

Funciones principales:

* Parsing HTML
* Extracción de noticias
* Control de rastreo
* Paginación

---

### modules/nlp/

Implementa el procesamiento de lenguaje natural.

Funciones principales:

* Limpieza de texto
* Tokenización
* Stopwords
* Stemming
* TF-IDF
* Control de calidad del corpus

---

### modules/classification/

Implementa el análisis automático de noticias.

Funciones principales:

* Clasificación temática
* Análisis de sentimientos
* Selección automática de modelos

---

### modules/search/

Implementa el motor de búsqueda.

Funciones principales:

* Índice invertido
* Búsqueda booleana
* Búsqueda vectorial
* Evaluación del buscador
* Sistema de alertas

---

### modules/chatbot/

Implementa el sistema conversacional.

Funciones principales:

* Chatbot basado en similitud
* Preguntas y respuestas
* Memoria de contexto

---

### modules/semantic/

Implementa la capa semántica del proyecto.

Funciones principales:

* Construcción del Knowledge Graph
* Consultas SPARQL
* Enlaces con Wikidata
* Datasets abiertos
* Validación SHACL

---

### modules/reports/

Genera los reportes automáticos del sistema.

Funciones principales:

* Reporte final
* Manifiesto de ejecución
* Estadísticas
* Exportación de resultados

---

### modules/analytics/

Módulos adicionales de análisis.

Funciones principales:

* Tendencias temporales
* Línea de tiempo
* Detección de picos
* Estadísticas avanzadas

---

## outputs/

Contiene todos los resultados generados por el sistema.

### outputs/reports/

Reportes automáticos.

Ejemplos:

* reporte_final_simanw.txt
* manifiesto_ejecucion.json
* reporte_kg.json
* reporte_sentimiento.json

### outputs/alerts/

Historial de alertas generadas.

### outputs/evaluations/

Resultados de evaluación del buscador y clasificadores.

---

# Funcionalidades implementadas

## Fase 1

Rastreo y extracción automática de noticias.

## Fase 2

Procesamiento de lenguaje natural.

## Fase 3

Clasificación automática y análisis de sentimientos.

## Fase 4

Motor de búsqueda inteligente.

## Fase 5

Chatbot y sistema Question & Answering.

## Fase 6

Knowledge Graph y Web Semántica.

## Fase 7

Generación automática de reportes.

---

# Tecnologías utilizadas

* Python
* Streamlit
* BeautifulSoup
* Pandas
* Scikit-Learn
* NLTK
* RDFLib
* Plotly
* JSON-LD
* SPARQL

---

# Autor

Sebastián Asís Sosa Santiago

Instituto Tecnológico de Morelia

Ingeniería en Sistemas Computacionales

Proyecto académico desarrollado para la materia de Recuperación de Información Web.
