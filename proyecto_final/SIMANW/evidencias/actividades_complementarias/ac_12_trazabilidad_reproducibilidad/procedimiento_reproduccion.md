# Procedimiento de reproducción del SIMANW

## Requisitos

* Python 3.13 o superior
* pip
* Conexión a Internet (solo para rastreo real y consultas SPARQL externas)

## Instalación

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

### Paso 1: Rastreo

```bash
python fase_1_rastreo.py
```

Salida:

```text
noticias_simanw.json
```

### Paso 2: Control de calidad

```bash
python ac_8_control_calidad_corpus.py
```

Salida:

```text
corpus_depurado.json
informe_calidad_corpus.json
```

### Paso 3: NLP

```bash
python fase_2_pipeline_nlp.py
```

### Paso 4: Clasificación y análisis

```bash
python fase_3_clasificacion.py
```

### Paso 5: Motor de búsqueda

```bash
python fase_4_busqueda.py
```

### Paso 6: Chatbot y QA

```bash
python fase_5_chatbot.py
```

### Paso 7: Knowledge Graph

```bash
python fase_6_knowledge_graph.py
```

### Paso 8: Reporte final

```bash
python fase_7_reportes.py
```

## Resultado esperado

El sistema debe generar:

* Corpus rastreado
* Corpus depurado
* Índice de búsqueda
* Knowledge Graph RDF
* Reporte final del SIMANW
