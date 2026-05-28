# Proyecto: Sistema Inteligente de Monitoreo y Análisis de Noticias Web 2026 Enero Junio

## Descripción del Proyecto

El alumno desarrollará un Sistema Inteligente de Monitoreo y Análisis de Noticias Web (SIMANW). Este es un sistema completo que:
- Rastrea noticias de portales web automáticamente
- Procesa el texto con técnicas de lenguaje natural
- Clasifica las noticias por categoría y sentimiento
- Permite búsquedas inteligentes en lenguaje natural
- Detecta temas de conversación y sugiere contenido relacionado
- Almacena todo en un grafo de conocimiento semántico consultable
- Genera reportes automáticos y responde preguntas sobre los datos

El proyecto se construye de forma incremental: cada fase agrega funcionalidad al sistema y cubre los temas del programa. Al final, todas las piezas se integran en un pipeline funcional.

Arquitectura del Sistema SIMANW:

  ┌─────────────────────────────────────────────────────────────────┐
  │                         SIMANW                                  │
  │                                                                 │
  │  [Fase 1: Rastreo] ──→ [Fase 2: NLP] ──→ [Fase 3: Análisis]     │
  │         │                     │                    │            │
  │         ▼                     ▼                    ▼            │
  │  [Fase 4: Motor de Búsqueda] ←──── [Fase 5: Conversación]       │
  │         │                                          │            │
  │         ▼                                          ▼            │
  │  [Fase 6: Knowledge Graph Semántico + Datos Abiertos]           │
  │         │                                                       │
  │         ▼                                                       │
  │  [Fase 7: Reportes + Q&A]                                       │
  └─────────────────────────────────────────────────────────────────┘

## Dependencias del proyecto
```python
import subprocess, sys

dependencias = [
    'nltk', 'scikit-learn', 'numpy', 'pandas',
    'beautifulsoup4', 'requests', 'scrapy',
    'rdflib', 'SPARQLWrapper', 'transformers',
    'matplotlib'
]

for dep in dependencias:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('vader_lexicon', quiet=True)
```

## Fase 1: Rastreador Web de Noticias

En esta fase el alumno construye el módulo de extracción automática de información de la web. El sistema necesita obtener noticias de forma autónoma, lo cual requiere entender el DOM HTML, definir el alcance del rastreo, y almacenar los datos extraídos.

### 1.1 Entendiendo el DOM y HTML Parsing

Lo primero es poder leer y navegar la estructura de una página web. El alumno implementa un parser que entiende la jerarquía del DOM.

```python
from bs4 import BeautifulSoup

html_portal_noticias = """
<!DOCTYPE html>
<html>
<head><title>Portal de Noticias - SIMANW</title></head>
<body>
  <nav><a href="/">Inicio</a> <a href="/tech">Tech</a> <a href="/ciencia">Ciencia</a></nav>
  <main id="contenido">
    <h1>Últimas Noticias</h1>
    <article class="noticia" data-categoria="tecnologia">
      <h2>Avances en IA Generativa revolucionan la industria</h2>
      <p class="cuerpo">Los nuevos modelos de inteligencia artificial generativa
      están transformando múltiples industrias. Empresas de todo el mundo adoptan
      estas tecnologías para automatizar procesos creativos y analíticos.</p>
      <div class="meta">
        <span class="fecha">2026-05-10</span>
        <span class="autor">María García</span>
        <a href="/noticias/ia-generativa-2026" class="leer-mas">Leer más</a>
      </div>
    </article>
    <article class="noticia" data-categoria="economia">
      <h2>Mercados financieros muestran volatilidad ante incertidumbre global</h2>
      <p class="cuerpo">Los principales índices bursátiles registraron caídas
      significativas. Analistas señalan que la inflación persistente y las
      tensiones geopolíticas generan preocupación entre los inversores.</p>
      <div class="meta">
        <span class="fecha">2026-05-09</span>
        <span class="autor">Carlos Ruiz</span>
        <a href="/noticias/mercados-volatilidad" class="leer-mas">Leer más</a>
      </div>
    </article>
    <article class="noticia" data-categoria="ciencia">
      <h2>Descubrimiento científico sobre cambio climático alarma a expertos</h2>
      <p class="cuerpo">Un equipo internacional de investigadores publicó un
      estudio que revela datos preocupantes sobre el ritmo del calentamiento
      global. Los resultados superan las peores predicciones anteriores.</p>
      <div class="meta">
        <span class="fecha">2026-05-08</span>
        <span class="autor">Ana López</span>
        <a href="/noticias/clima-estudio-2026" class="leer-mas">Leer más</a>
      </div>
    </article>
    <article class="noticia" data-categoria="tecnologia">
      <h2>Python 3.14 trae mejoras significativas en rendimiento</h2>
      <p class="cuerpo">La nueva versión del lenguaje de programación Python
      incluye optimizaciones que mejoran la velocidad de ejecución hasta en un
      40%. La comunidad de desarrolladores celebra estos avances.</p>
      <div class="meta">
        <span class="fecha">2026-05-07</span>
        <span class="autor">Juan Hernández</span>
        <a href="/noticias/python-314" class="leer-mas">Leer más</a>
      </div>
    </article>
    <article class="noticia" data-categoria="gobierno">
      <h2>Gobierno lanza portal de datos abiertos con tecnología semántica</h2>
      <p class="cuerpo">La nueva plataforma gubernamental ofrece acceso a
      datasets públicos en formatos RDF y JSON-LD. Ciudadanos y desarrolladores
      pueden consultar información presupuestal y estadísticas mediante SPARQL.</p>
      <div class="meta">
        <span class="fecha">2026-05-06</span>
        <span class="autor">Pedro Sánchez</span>
        <a href="/noticias/datos-abiertos-gob" class="leer-mas">Leer más</a>
      </div>
    </article>
  </main>
  <aside>
    <h3>Tendencias</h3>
    <ul>
      <li><a href="/trend/1">#InteligenciaArtificial</a></li>
      <li><a href="/trend/2">#Python</a></li>
      <li><a href="/trend/3">#DatosAbiertos</a></li>
    </ul>
  </aside>
  <footer><p>© 2026 Portal SIMANW</p></footer>
</body>
</html>
"""

soup = BeautifulSoup(html_portal_noticias, 'html.parser')

print("=== FASE 1.1: Parsing del DOM ===\n")
print(f"Título del portal: {soup.title.string}")
print(f"Secciones de navegación: {[a.string for a in soup.nav.find_all('a')]}")
print(f"Total de artículos: {len(soup.find_all('article'))}")
print(f"Tendencias: {[li.a.string for li in soup.aside.find_all('li')]}")

print("\nEstructura del DOM detectada:")
print(f"  <html>")
print(f"    <head> → título")
print(f"    <body>")
print(f"      <nav> → {len(soup.nav.find_all('a'))} enlaces")
print(f"      <main> → {len(soup.main.find_all('article'))} artículos")
print(f"      <aside> → tendencias")
print(f"      <footer> → copyright")
```

### 1.2 Extractor de noticias (Spider)

El alumno construye el extractor que sabe navegar la estructura HTML del portal y obtener los datos estructurados de cada noticia.

```python
class ExtractorNoticias:
    """
    Componente del SIMANW que extrae noticias de páginas HTML.
    En producción usaría Scrapy; aquí se muestra la lógica central.
    """

    def __init__(self):
        self.noticias_extraidas = []
        self.errores = []

    def extraer_de_html(self, html_content, url_base="https://portal.com"):
        """Extrae todas las noticias de una página HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        articulos = soup.find_all('article', class_='noticia')

        for art in articulos:
            try:
                noticia = {
                    'titulo': art.find('h2').get_text(strip=True),
                    'cuerpo': art.find('p', class_='cuerpo').get_text(strip=True),
                    'fecha': art.find('span', class_='fecha').get_text(strip=True),
                    'autor': art.find('span', class_='autor').get_text(strip=True),
                    'categoria_original': art.get('data-categoria', 'sin_categoria'),
                    'url': url_base + art.find('a', class_='leer-mas')['href'],
                    'fuente': url_base,
                }
                self.noticias_extraidas.append(noticia)
            except Exception as e:
                self.errores.append(str(e))

        return self.noticias_extraidas

    def resumen_extraccion(self):
        return {
            'total_extraidas': len(self.noticias_extraidas),
            'errores': len(self.errores),
            'categorias': list(set(n['categoria_original'] for n in self.noticias_extraidas)),
            'rango_fechas': (
                min(n['fecha'] for n in self.noticias_extraidas),
                max(n['fecha'] for n in self.noticias_extraidas)
            ) if self.noticias_extraidas else None
        }


extractor = ExtractorNoticias()
noticias = extractor.extraer_de_html(html_portal_noticias)

print("=== FASE 1.2: Extracción de Noticias ===\n")
resumen = extractor.resumen_extraccion()
print(f"Noticias extraídas: {resumen['total_extraidas']}")
print(f"Errores: {resumen['errores']}")
print(f"Categorías encontradas: {resumen['categorias']}")
print(f"Rango de fechas: {resumen['rango_fechas']}")

print("\nNoticias:")
for i, n in enumerate(noticias, 1):
    print(f"  {i}. [{n['fecha']}] [{n['categoria_original']}] {n['titulo'][:60]}")
    print(f"     Autor: {n['autor']} | URL: {n['url']}")
```

### 1.3 Alcance y control del rastreo

El sistema necesita definir límites: qué URLs puede visitar, cuántas páginas rastrear, y respetar las reglas del sitio.

```python
from urllib.parse import urlparse, urljoin
from collections import deque

class ControlRastreo:
    """Controla el alcance y la política del rastreador."""

    def __init__(self, url_semilla, modo='dominio', max_paginas=50, delay=2):
        self.url_semilla = url_semilla
        self.dominio = urlparse(url_semilla).netloc
        self.modo = modo
        self.max_paginas = max_paginas
        self.delay = delay
        self.visitadas = set()
        self.cola = deque([url_semilla])
        self.rechazadas = []

    def url_permitida(self, url):
        """Verifica si una URL está dentro del alcance definido."""
        parsed = urlparse(url)
        if self.modo == 'dominio':
            return parsed.netloc == self.dominio
        elif self.modo == 'directorio':
            base_path = urlparse(self.url_semilla).path.rsplit('/', 1)[0]
            return parsed.netloc == self.dominio and parsed.path.startswith(base_path)
        elif self.modo == 'subdominio':
            return parsed.netloc.endswith(self.dominio.split('.', 1)[-1])
        return False

    def registrar_visita(self, url):
        self.visitadas.add(url)

    def agregar_enlaces(self, enlaces):
        """Agrega enlaces descubiertos a la cola si son válidos."""
        agregados = 0
        for enlace in enlaces:
            url_abs = urljoin(self.url_semilla, enlace)
            if url_abs not in self.visitadas and self.url_permitida(url_abs):
                self.cola.append(url_abs)
                agregados += 1
            else:
                self.rechazadas.append(url_abs)
        return agregados

    def siguiente(self):
        """Obtiene la siguiente URL a visitar."""
        if self.cola and len(self.visitadas) < self.max_paginas:
            url = self.cola.popleft()
            self.registrar_visita(url)
            return url
        return None

    def estado(self):
        return {
            'visitadas': len(self.visitadas),
            'en_cola': len(self.cola),
            'rechazadas': len(self.rechazadas),
            'limite': self.max_paginas,
            'completado': len(self.visitadas) >= self.max_paginas or not self.cola
        }


control = ControlRastreo("https://portal-noticias.com/noticias/", modo='directorio', max_paginas=10)

enlaces_descubiertos = [
    "/noticias/pagina/2",
    "/noticias/tecnologia/ia-2026",
    "/deportes/futbol-liga",
    "https://otro-sitio.com/articulo",
    "/noticias/economia/mercados",
    "/noticias/ciencia/clima",
    "/contacto",
]

print("=== FASE 1.3: Control de Rastreo ===\n")
print(f"URL semilla: {control.url_semilla}")
print(f"Modo: {control.modo} | Máx páginas: {control.max_paginas}")
print(f"Delay entre peticiones: {control.delay}s")

agregados = control.agregar_enlaces(enlaces_descubiertos)
print(f"\nEnlaces descubiertos: {len(enlaces_descubiertos)}")
print(f"Agregados a la cola: {agregados}")
print(f"Rechazados: {len(control.rechazadas)}")

print("\nSimulación de rastreo:")
while True:
    url = control.siguiente()
    if not url:
        break
    print(f"  Visitando: {url}")

estado = control.estado()
print(f"\nEstado final: {estado}")
```

### 1.4 Estructura del spider en Scrapy (producción)

Así se vería el rastreador en un entorno real con Scrapy:

```python
scrapy_code = '''
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SIMANWSpider(CrawlSpider):
    """Spider del SIMANW para producción."""
    name = 'simanw_noticias'
    allowed_domains = ['portal-noticias.com']
    start_urls = ['https://portal-noticias.com/noticias/']

    rules = (
        Rule(LinkExtractor(allow=r'/noticias/'), callback='parse_noticia', follow=True),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 4,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'noticias_%(time)s.json',
    }

    def parse_noticia(self, response):
        for articulo in response.css('article.noticia'):
            yield {
                'titulo': articulo.css('h2::text').get(),
                'cuerpo': articulo.css('p.cuerpo::text').get(),
                'fecha': articulo.css('span.fecha::text').get(),
                'autor': articulo.css('span.autor::text').get(),
                'categoria': articulo.attrib.get('data-categoria'),
                'url': response.url,
            }
'''
print("=== Código Scrapy para producción ===")
print(scrapy_code)
print("# Ejecución: scrapy crawl simanw_noticias")
```

## Fase 2: Procesamiento de Lenguaje Natural

Ahora que el sistema tiene noticias crudas, necesita procesarlas para poder trabajar con ellas computacionalmente. Aquí el alumno construye el pipeline NLP del SIMANW.

### 2.1 Pipeline de pre-procesamiento

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from collections import Counter

class PipelineNLP:
    """Pipeline de procesamiento de lenguaje natural del SIMANW."""

    def __init__(self, idioma='spanish'):
        self.idioma = idioma
        self.stemmer = SnowballStemmer(idioma)
        self.stop_words = set(stopwords.words(idioma))

    def limpiar(self, texto):
        """Paso 1: Limpieza básica."""
        texto = texto.lower()
        texto = re.sub(r'[^\w\sáéíóúñü]', ' ', texto)
        texto = re.sub(r'\d+', '', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    def tokenizar(self, texto):
        """Paso 2: Tokenización."""
        return word_tokenize(texto, language=self.idioma)

    def eliminar_stopwords(self, tokens):
        """Paso 3: Eliminar palabras vacías."""
        return [t for t in tokens if t not in self.stop_words and len(t) > 2]

    def aplicar_stemming(self, tokens):
        """Paso 4: Reducir a raíz (stem)."""
        return [self.stemmer.stem(t) for t in tokens]

    def procesar(self, texto):
        """Ejecuta el pipeline completo."""
        limpio = self.limpiar(texto)
        tokens = self.tokenizar(limpio)
        sin_sw = self.eliminar_stopwords(tokens)
        stems = self.aplicar_stemming(sin_sw)
        return {
            'original': texto,
            'limpio': limpio,
            'tokens': tokens,
            'sin_stopwords': sin_sw,
            'stems': stems,
            'num_oraciones': len(sent_tokenize(texto, language=self.idioma)),
            'vocabulario_unico': len(set(sin_sw)),
            'riqueza_lexica': len(set(sin_sw)) / max(len(sin_sw), 1)
        }

    def estadisticas_corpus(self, textos_procesados):
        """Genera estadísticas del corpus completo."""
        todos_tokens = []
        todos_stems = []
        for tp in textos_procesados:
            todos_tokens.extend(tp['sin_stopwords'])
            todos_stems.extend(tp['stems'])
        return {
            'total_documentos': len(textos_procesados),
            'total_tokens': len(todos_tokens),
            'vocabulario_total': len(set(todos_tokens)),
            'stems_unicos': len(set(todos_stems)),
            'palabras_frecuentes': Counter(todos_tokens).most_common(10),
            'promedio_tokens_doc': len(todos_tokens) / max(len(textos_procesados), 1)
        }


pipeline = PipelineNLP()

print("=== FASE 2.1: Pipeline NLP ===\n")
print("Procesando noticias extraídas...\n")

noticias_procesadas = []
for noticia in noticias:
    texto_completo = f"{noticia['titulo']}. {noticia['cuerpo']}"
    resultado = pipeline.procesar(texto_completo)
    noticia['nlp'] = resultado
    noticias_procesadas.append(resultado)
    print(f"  [{noticia['categoria_original']}] {noticia['titulo'][:50]}...")
    print(f"    Tokens: {len(resultado['tokens'])} → Sin SW: {len(resultado['sin_stopwords'])} → Stems: {len(resultado['stems'])}")
    print(f"    Riqueza léxica: {resultado['riqueza_lexica']:.3f}")
    print()

stats = pipeline.estadisticas_corpus(noticias_procesadas)
print("--- Estadísticas del Corpus ---")
for k, v in stats.items():
    if k != 'palabras_frecuentes':
        print(f"  {k}: {v}")
print(f"\n  Palabras más frecuentes:")
for palabra, freq in stats['palabras_frecuentes']:
    print(f"    '{palabra}': {freq}")
```

### 2.2 Representación vectorial (TF-IDF)

El sistema convierte las noticias en vectores numéricos para poder compararlas matemáticamente.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class RepresentacionVectorial:
    """Convierte los documentos del SIMANW en vectores TF-IDF."""

    def __init__(self, max_features=2000, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True
        )
        self.matriz = None
        self.documentos_texto = []

    def construir_matriz(self, documentos):
        """Construye la matriz TF-IDF a partir de textos pre-procesados."""
        self.documentos_texto = documentos
        self.matriz = self.vectorizer.fit_transform(documentos)
        return self.matriz

    def vocabulario(self):
        return self.vectorizer.get_feature_names_out()

    def top_terminos_documento(self, doc_idx, n=8):
        """Términos más importantes de un documento."""
        vector = self.matriz[doc_idx].toarray().flatten()
        terminos = self.vocabulario()
        indices_top = vector.argsort()[::-1][:n]
        return [(terminos[i], vector[i]) for i in indices_top if vector[i] > 0]

    def info_matriz(self):
        return {
            'documentos': self.matriz.shape[0],
            'features': self.matriz.shape[1],
            'densidad': self.matriz.nnz / (self.matriz.shape[0] * self.matriz.shape[1]),
            'terminos_promedio_doc': self.matriz.nnz / self.matriz.shape[0]
        }


# Usar textos pre-procesados (sin stopwords, reunidos)
textos_para_vectorizar = [' '.join(n['nlp']['sin_stopwords']) for n in noticias]

representacion = RepresentacionVectorial()
representacion.construir_matriz(textos_para_vectorizar)

print("=== FASE 2.2: Representación Vectorial TF-IDF ===\n")
info = representacion.info_matriz()
print(f"Matriz TF-IDF: {info['documentos']} docs × {info['features']} features")
print(f"Densidad: {info['densidad']:.4f}")
print(f"Términos promedio por documento: {info['terminos_promedio_doc']:.1f}")

print(f"\nVocabulario (muestra): {list(representacion.vocabulario()[:15])}")

print("\nTérminos más relevantes por noticia:")
for i, noticia in enumerate(noticias):
    print(f"\n  [{noticia['categoria_original']}] {noticia['titulo'][:45]}...")
    top = representacion.top_terminos_documento(i, n=5)
    for termino, peso in top:
        print(f"    {termino:<20} = {peso:.4f}")
```

### 2.3 Cálculo de similitud entre noticias

Con los vectores, el sistema puede determinar qué noticias son parecidas entre sí.

```python
from sklearn.metrics.pairwise import cosine_similarity

class CalculadorSimilitud:
    """Calcula similitudes entre documentos del SIMANW."""

    def __init__(self, matriz_tfidf):
        self.matriz = matriz_tfidf
        self.sim_matrix = cosine_similarity(matriz_tfidf)

    def similitud_par(self, doc_i, doc_j):
        return self.sim_matrix[doc_i][doc_j]

    def documentos_similares(self, doc_idx, top_n=3):
        """Encuentra los documentos más similares a uno dado."""
        similitudes = self.sim_matrix[doc_idx]
        indices = similitudes.argsort()[::-1][1:top_n+1]
        return [(idx, similitudes[idx]) for idx in indices]

    def agrupar_por_similitud(self, umbral=0.15):
        """Agrupa documentos que superen un umbral de similitud."""
        grupos = []
        visitados = set()
        for i in range(len(self.sim_matrix)):
            if i in visitados:
                continue
            grupo = [i]
            visitados.add(i)
            for j in range(i+1, len(self.sim_matrix)):
                if j not in visitados and self.sim_matrix[i][j] >= umbral:
                    grupo.append(j)
                    visitados.add(j)
            grupos.append(grupo)
        return grupos


calculador = CalculadorSimilitud(representacion.matriz)

print("=== FASE 2.3: Similitud entre Noticias ===\n")
print("Matriz de similitud coseno:")
print(f"{'':>5}", end="")
for i in range(len(noticias)):
    print(f"{'N'+str(i+1):>7}", end="")
print()
for i in range(len(noticias)):
    print(f"N{i+1:>3}", end=" ")
    for j in range(len(noticias)):
        print(f"{calculador.similitud_par(i,j):>7.3f}", end="")
    print()

print("\nNoticias más similares entre sí:")
for i, noticia in enumerate(noticias):
    similares = calculador.documentos_similares(i, top_n=1)
    if similares:
        j, sim = similares[0]
        if sim > 0.05:
            print(f"  N{i+1} ↔ N{j+1} (sim={sim:.3f})")
            print(f"    '{noticia['titulo'][:40]}...'")
            print(f"    '{noticias[j]['titulo'][:40]}...'")

print("\nGrupos temáticos detectados:")
grupos = calculador.agrupar_por_similitud(umbral=0.1)
for g_idx, grupo in enumerate(grupos):
    print(f"  Grupo {g_idx+1}: {['N'+str(i+1) for i in grupo]}")
    for i in grupo:
        print(f"    - {noticias[i]['titulo'][:50]}")
```

## Fase 3: Clasificación y Análisis Automático

El sistema ahora debe categorizar automáticamente cada noticia y analizar su tono (sentimiento). También detecta temas en conversaciones para poder orientar publicidad.

### 3.1 Clasificador automático de noticias

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import numpy as np

class ClasificadorNoticias:
    """Clasifica noticias automáticamente por categoría."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.clasificador = LinearSVC(max_iter=2000)
        self.categorias = []
        self.entrenado = False

    def entrenar(self, textos, etiquetas):
        """Entrena el clasificador con datos etiquetados."""
        X = self.vectorizer.fit_transform(textos)
        self.clasificador.fit(X, etiquetas)
        self.categorias = list(set(etiquetas))
        self.entrenado = True

        scores = cross_val_score(self.clasificador, X, etiquetas, cv=min(3, len(textos)//2))
        return {
            'accuracy_cv': scores.mean(),
            'categorias': self.categorias,
            'n_muestras': len(textos)
        }

    def predecir(self, textos):
        """Predice la categoría de nuevos textos."""
        X = self.vectorizer.transform(textos)
        return self.clasificador.predict(X)

    def predecir_con_confianza(self, texto):
        """Predice con scores de decisión."""
        X = self.vectorizer.transform([texto])
        decision = self.clasificador.decision_function(X)[0]
        prediccion = self.clasificador.predict(X)[0]
        return prediccion, dict(zip(self.clasificador.classes_, decision))


# Datos de entrenamiento (en producción vendrían del rastreo acumulado)
textos_entrenamiento = [
    "inteligencia artificial machine learning algoritmos redes neuronales deep learning",
    "nuevo procesador computadora software desarrollo programación tecnología",
    "startup tecnológica lanza aplicación innovadora plataforma digital",
    "robot automatización industria software empresa tecnología",
    "mercados financieros bolsa acciones inversión capital rendimiento",
    "inflación economía banco central tasas interés política monetaria",
    "desempleo crisis económica recesión PIB crecimiento producto interno",
    "comercio internacional exportaciones importaciones aranceles tratado",
    "estudio científico investigadores descubrimiento laboratorio publicación",
    "cambio climático calentamiento global temperatura emisiones carbono",
    "vacuna tratamiento médico salud enfermedad hospital pacientes",
    "espacio NASA cohete satélite misión exploración astronauta",
    "elecciones candidato presidente congreso voto democracia partido",
    "gobierno ley reforma política pública decreto legislación",
    "seguridad pública policía crimen delito justicia tribunal",
    "presupuesto gasto público programa social gobierno federal",
]

etiquetas_entrenamiento = [
    'tecnologia', 'tecnologia', 'tecnologia', 'tecnologia',
    'economia', 'economia', 'economia', 'economia',
    'ciencia', 'ciencia', 'ciencia', 'ciencia',
    'politica', 'politica', 'politica', 'politica',
]

clasificador = ClasificadorNoticias()
resultado_entrenamiento = clasificador.entrenar(textos_entrenamiento, etiquetas_entrenamiento)

print("=== FASE 3.1: Clasificador de Noticias ===\n")
print(f"Entrenamiento completado:")
print(f"  Muestras: {resultado_entrenamiento['n_muestras']}")
print(f"  Categorías: {resultado_entrenamiento['categorias']}")
print(f"  Accuracy (CV): {resultado_entrenamiento['accuracy_cv']:.3f}")

print("\nClasificación automática de noticias del SIMANW:")
for noticia in noticias:
    texto = f"{noticia['titulo']} {noticia['cuerpo']}"
    prediccion, scores = clasificador.predecir_con_confianza(texto)
    noticia['categoria_predicha'] = prediccion
    print(f"\n  Título: {noticia['titulo'][:55]}...")
    print(f"  Cat. original: {noticia['categoria_original']} | Predicha: {prediccion}")
    top_scores = sorted(scores.items(), key=lambda x: -x[1])[:3]
    print(f"  Scores: {', '.join(f'{c}={s:.2f}' for c,s in top_scores)}")
```

### 3.2 Análisis de sentimientos

El SIMANW necesita saber si las noticias tienen un tono positivo, negativo o neutral para generar reportes de percepción.

```python
from nltk.sentiment import SentimentIntensityAnalyzer

class AnalizadorSentimientos:
    """Analiza el sentimiento de las noticias del SIMANW."""

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analizar(self, texto):
        scores = self.sia.polarity_scores(texto)
        compound = scores['compound']
        if compound >= 0.05:
            etiqueta = 'positivo'
        elif compound <= -0.05:
            etiqueta = 'negativo'
        else:
            etiqueta = 'neutral'
        return {
            'positivo': scores['pos'],
            'negativo': scores['neg'],
            'neutral': scores['neu'],
            'compound': compound,
            'etiqueta': etiqueta
        }

    def analizar_corpus(self, documentos):
        """Analiza sentimiento de un conjunto de documentos."""
        resultados = [self.analizar(doc) for doc in documentos]
        distribucion = Counter(r['etiqueta'] for r in resultados)
        promedio = sum(r['compound'] for r in resultados) / len(resultados)
        return resultados, {
            'distribucion': dict(distribucion),
            'sentimiento_promedio': promedio,
            'tono_general': 'positivo' if promedio > 0.05 else 'negativo' if promedio < -0.05 else 'neutral'
        }


analizador_sent = AnalizadorSentimientos()

print("=== FASE 3.2: Análisis de Sentimientos ===\n")
textos_noticias = [n['cuerpo'] for n in noticias]
resultados_sent, resumen_sent = analizador_sent.analizar_corpus(textos_noticias)

for i, (noticia, sent) in enumerate(zip(noticias, resultados_sent)):
    noticia['sentimiento'] = sent
    indicador = "↑" if sent['etiqueta'] == 'positivo' else "↓" if sent['etiqueta'] == 'negativo' else "→"
    print(f"  {indicador} [{sent['compound']:+.3f}] {noticia['titulo'][:55]}")

print(f"\n--- Resumen de Sentimiento del Corpus ---")
print(f"  Distribución: {resumen_sent['distribucion']}")
print(f"  Promedio: {resumen_sent['sentimiento_promedio']:+.3f}")
print(f"  Tono general: {resumen_sent['tono_general'].upper()}")
```

### 3.3 Sistema de recomendación por contenido

El SIMANW recomienda noticias relacionadas al usuario basándose en similitud de contenido.

```python
class SistemaRecomendacion:
    """Recomienda noticias relacionadas basándose en contenido."""

    def __init__(self, noticias, matriz_similitud):
        self.noticias = noticias
        self.sim_matrix = matriz_similitud

    def recomendar(self, noticia_idx, top_n=2, excluir_misma_cat=False):
        """Recomienda noticias similares."""
        similitudes = self.sim_matrix[noticia_idx]
        candidatos = []
        for i, sim in enumerate(similitudes):
            if i == noticia_idx:
                continue
            if excluir_misma_cat and \
               self.noticias[i]['categoria_original'] == self.noticias[noticia_idx]['categoria_original']:
                continue
            candidatos.append((i, sim))
        candidatos.sort(key=lambda x: -x[1])
        return candidatos[:top_n]

    def recomendar_por_perfil(self, indices_leidos, top_n=3):
        """Recomienda basándose en múltiples noticias leídas (perfil de usuario)."""
        sim_acumulada = np.zeros(len(self.noticias))
        for idx in indices_leidos:
            sim_acumulada += self.sim_matrix[idx]
        for idx in indices_leidos:
            sim_acumulada[idx] = 0
        mejores = sim_acumulada.argsort()[::-1][:top_n]
        return [(i, sim_acumulada[i]) for i in mejores if sim_acumulada[i] > 0]


recomendador = SistemaRecomendacion(noticias, calculador.sim_matrix)

print("=== FASE 3.3: Sistema de Recomendación ===\n")
print("Si leíste esta noticia, te recomendamos:")
for i in range(len(noticias)):
    recomendaciones = recomendador.recomendar(i, top_n=2)
    print(f"\n  Leíste: '{noticias[i]['titulo'][:50]}...'")
    for j, sim in recomendaciones:
        print(f"    → [{sim:.3f}] {noticias[j]['titulo'][:50]}...")

print("\n\nRecomendación por perfil (si leyó noticias 1 y 4 - tecnología):")
perfil_recs = recomendador.recomendar_por_perfil([0, 3], top_n=2)
for idx, score in perfil_recs:
    print(f"  → [{score:.3f}] {noticias[idx]['titulo'][:55]}")
```

### 3.4 Detección de temas en conversación para publicidad dirigida

El SIMANW incluye un componente de chat donde los usuarios discuten noticias. El sistema detecta el tema de la conversación para mostrar publicidad relevante.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

class DetectorTemasPublicidad:
    """
    Detecta el tema de una conversación en tiempo real
    y sugiere publicidad dirigida.
    """

    def __init__(self):
        self.mensajes = []
        self.catalogo_publicidad = {
            'tecnologia': [
                "Curso de IA y Machine Learning - 50% descuento",
                "Laptop para programadores - i9 + 32GB RAM",
                "Conferencia Tech 2026 - Boletos disponibles",
            ],
            'economia': [
                "App de inversiones - Comienza con $100",
                "Curso de finanzas personales gratuito",
                "Tarjeta de crédito sin anualidad",
            ],
            'ciencia': [
                "Suscripción a revista científica digital",
                "Telescopio astronómico - envío gratis",
                "Curso de ciencia de datos online",
            ],
            'politica': [
                "Portal de transparencia gubernamental",
                "Notificaciones de cambios legislativos",
                "Foro de participación ciudadana",
            ],
        }
        self.perfiles_tema = None
        self._construir_perfiles()

    def _construir_perfiles(self):
        """Construye vectores representativos de cada tema."""
        temas_texto = {
            'tecnologia': "inteligencia artificial programación software apps tecnología computadora robot digital innovación",
            'economia': "dinero inversión mercado bolsa finanzas banco economía empleo trabajo",
            'ciencia': "investigación científico descubrimiento estudio laboratorio clima universo",
            'politica': "gobierno elecciones presidente ley congreso partido democracia",
        }
        self.temas = list(temas_texto.keys())
        self.vec_temas = TfidfVectorizer()
        self.matriz_temas = self.vec_temas.fit_transform(temas_texto.values())

    def agregar_mensaje(self, usuario, texto):
        self.mensajes.append({'usuario': usuario, 'texto': texto})

    def detectar_tema(self, ventana=5):
        """Detecta el tema dominante en los últimos N mensajes."""
        if not self.mensajes:
            return 'general', 0.0

        ultimos = self.mensajes[-ventana:]
        texto_ventana = ' '.join(m['texto'] for m in ultimos)
        vec_conversacion = self.vec_temas.transform([texto_ventana])
        similitudes = cosine_similarity(vec_conversacion, self.matriz_temas)[0]

        mejor_idx = similitudes.argmax()
        return self.temas[mejor_idx], similitudes[mejor_idx]

    def obtener_publicidad(self, tema):
        """Selecciona publicidad para el tema detectado."""
        import random
        if tema in self.catalogo_publicidad:
            return random.choice(self.catalogo_publicidad[tema])
        return "Descubre las mejores ofertas del día"

    def simular_chat(self, conversacion):
        """Simula un chat completo con detección de publicidad."""
        resultados = []
        for usuario, mensaje in conversacion:
            self.agregar_mensaje(usuario, mensaje)
            tema, confianza = self.detectar_tema()
            publicidad = self.obtener_publicidad(tema)
            resultados.append({
                'usuario': usuario,
                'mensaje': mensaje,
                'tema': tema,
                'confianza': confianza,
                'publicidad': publicidad
            })
        return resultados


detector = DetectorTemasPublicidad()

conversacion_usuarios = [
    ("Laura", "¿Vieron la noticia sobre la nueva IA de Google?"),
    ("Miguel", "Sí, dicen que puede programar mejor que muchos desarrolladores"),
    ("Laura", "Me preocupa el futuro del trabajo en tecnología"),
    ("Roberto", "Yo creo que es una oportunidad, hay que aprender machine learning"),
    ("Miguel", "Cambiando de tema, ¿cómo ven la economía este trimestre?"),
    ("Laura", "Los mercados están muy volátiles, mis inversiones bajaron"),
    ("Roberto", "El banco central anunció que subirá las tasas de interés"),
    ("Miguel", "Mejor hay que diversificar, quizá invertir en fondos indexados"),
]

print("=== FASE 3.4: Detección de Temas + Publicidad ===\n")
print("Simulación de chat con publicidad dirigida:")
print("─" * 65)
resultados_chat = detector.simular_chat(conversacion_usuarios)

for r in resultados_chat:
    print(f"  [{r['usuario']}]: {r['mensaje']}")
    print(f"    Tema: {r['tema'].upper()} (confianza: {r['confianza']:.3f})")
    print(f"    Ad: {r['publicidad']}")
    print()

print("─" * 65)
temas_conv = Counter(r['tema'] for r in resultados_chat)
print(f"Resumen de temas en la conversación: {dict(temas_conv)}")
```

## Fase 4: Motor de Búsqueda Inteligente

El alumno construye el motor de búsqueda del SIMANW que permite a los usuarios encontrar noticias usando lenguaje natural, y evalúa su efectividad con métricas formales.

### 4.1 Índice invertido y búsqueda

```python
import math
from collections import Counter, defaultdict

class MotorBusqueda:
    """Motor de búsqueda del SIMANW con índice invertido y ranking TF-IDF."""

    def __init__(self):
        self.documentos = {}
        self.indice_invertido = defaultdict(dict)
        self.doc_lengths = {}
        self.N = 0
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.matriz_busqueda = None

    def indexar(self, documentos):
        """Construye el índice invertido."""
        self.N = len(documentos)
        textos = []
        for doc_id, doc in enumerate(documentos):
            self.documentos[doc_id] = doc
            texto = f"{doc['titulo']} {doc['cuerpo']}"
            textos.append(texto)
            tokens = texto.lower().split()
            tf = Counter(tokens)
            self.doc_lengths[doc_id] = len(tokens)
            for term, freq in tf.items():
                self.indice_invertido[term][doc_id] = freq

        self.matriz_busqueda = self.vectorizer.fit_transform(textos)

    def buscar_booleana(self, consulta, modo='AND'):
        """Búsqueda booleana simple."""
        terminos = consulta.lower().split()
        if modo == 'AND':
            result = set(self.indice_invertido.get(terminos[0], {}).keys()) if terminos else set()
            for t in terminos[1:]:
                result &= set(self.indice_invertido.get(t, {}).keys())
        else:  # OR
            result = set()
            for t in terminos:
                result |= set(self.indice_invertido.get(t, {}).keys())
        return list(result)

    def buscar_vectorial(self, consulta, top_k=5):
        """Búsqueda por similitud vectorial (ranking)."""
        consulta_vec = self.vectorizer.transform([consulta])
        similitudes = cosine_similarity(consulta_vec, self.matriz_busqueda)[0]
        indices = similitudes.argsort()[::-1][:top_k]
        resultados = []
        for idx in indices:
            if similitudes[idx] > 0:
                resultados.append({
                    'doc_id': idx,
                    'titulo': self.documentos[idx]['titulo'],
                    'relevancia': float(similitudes[idx]),
                    'categoria': self.documentos[idx].get('categoria_predicha',
                                 self.documentos[idx].get('categoria_original', '?')),
                    'sentimiento': self.documentos[idx].get('sentimiento', {}).get('etiqueta', '?'),
                    'snippet': self.documentos[idx]['cuerpo'][:80] + '...'
                })
        return resultados

    def info_indice(self):
        return {
            'documentos_indexados': self.N,
            'terminos_en_indice': len(self.indice_invertido),
            'tamano_promedio_posting': sum(len(v) for v in self.indice_invertido.values()) / max(len(self.indice_invertido), 1)
        }


motor = MotorBusqueda()
motor.indexar(noticias)

print("=== FASE 4.1: Motor de Búsqueda ===\n")
info = motor.info_indice()
print(f"Índice construido:")
print(f"  Documentos: {info['documentos_indexados']}")
print(f"  Términos únicos: {info['terminos_en_indice']}")
print(f"  Postings promedio: {info['tamano_promedio_posting']:.2f}")

consultas = [
    "inteligencia artificial tecnología",
    "mercados financieros economía",
    "datos abiertos gobierno semántica",
    "Python programación desarrollo",
    "cambio climático investigación científica",
]

print("\n--- Resultados de Búsqueda ---")
for consulta in consultas:
    resultados = motor.buscar_vectorial(consulta, top_k=2)
    print(f"\n  Consulta: '{consulta}'")
    for r in resultados:
        print(f"    [{r['relevancia']:.3f}] {r['titulo'][:50]}...")
        print(f"      Cat: {r['categoria']} | Sent: {r['sentimiento']}")
```

### 4.2 Evaluación del motor de búsqueda

```python
class EvaluadorIRS:
    """Evalúa la efectividad del motor de búsqueda del SIMANW."""

    @staticmethod
    def precision(recuperados, relevantes):
        recuperados = set(recuperados)
        relevantes = set(relevantes)
        tp = len(recuperados & relevantes)
        return tp / len(recuperados) if recuperados else 0

    @staticmethod
    def recall(recuperados, relevantes):
        recuperados = set(recuperados)
        relevantes = set(relevantes)
        tp = len(recuperados & relevantes)
        return tp / len(relevantes) if relevantes else 0

    @staticmethod
    def f1(precision, recall):
        if precision + recall == 0:
            return 0
        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def precision_at_k(ranking, relevantes, k):
        """Precision considerando solo los top-k resultados."""
        top_k = set(ranking[:k])
        relevantes = set(relevantes)
        return len(top_k & relevantes) / k

    @staticmethod
    def average_precision(ranking, relevantes):
        """Average Precision para un ranking."""
        relevantes = set(relevantes)
        suma = 0
        relevantes_encontrados = 0
        for i, doc in enumerate(ranking, 1):
            if doc in relevantes:
                relevantes_encontrados += 1
                suma += relevantes_encontrados / i
        return suma / len(relevantes) if relevantes else 0

    def evaluar_consulta(self, recuperados_ids, relevantes_ids, total_docs):
        """Evaluación completa de una consulta."""
        p = self.precision(recuperados_ids, relevantes_ids)
        r = self.recall(recuperados_ids, relevantes_ids)
        f = self.f1(p, r)
        ap = self.average_precision(recuperados_ids, relevantes_ids)
        return {
            'precision': p,
            'recall': r,
            'f1': f,
            'average_precision': ap
        }


evaluador = EvaluadorIRS()

# Evaluación simulada: para "inteligencia artificial", las noticias 0 y 3 son relevantes
evaluaciones = [
    {'consulta': 'inteligencia artificial', 'relevantes': [0, 3], 'recuperados': [0, 3, 1]},
    {'consulta': 'economía mercados', 'relevantes': [1], 'recuperados': [1, 4, 2]},
    {'consulta': 'datos gobierno', 'relevantes': [4], 'recuperados': [4, 2]},
]

print("=== FASE 4.2: Evaluación del Motor de Búsqueda ===\n")
print(f"{'Consulta':<25} {'Precision':>10} {'Recall':>10} {'F1':>10} {'AP':>10}")
print("─" * 67)

map_total = 0
for ev in evaluaciones:
    metricas = evaluador.evaluar_consulta(ev['recuperados'], ev['relevantes'], len(noticias))
    map_total += metricas['average_precision']
    print(f"{ev['consulta']:<25} {metricas['precision']:>10.3f} {metricas['recall']:>10.3f} "
          f"{metricas['f1']:>10.3f} {metricas['average_precision']:>10.3f}")

map_score = map_total / len(evaluaciones)
print(f"\n  MAP (Mean Average Precision): {map_score:.3f}")

print("\n--- Precision@K para 'inteligencia artificial' ---")
ranking = [0, 3, 1, 2, 4]
relevantes = [0, 3]
for k in range(1, 6):
    pk = evaluador.precision_at_k(ranking, relevantes, k)
    print(f"  P@{k} = {pk:.3f}")
```

### 4.3 Búsqueda en lenguaje natural (como consultar una base de datos)

El usuario puede hacer preguntas naturales y el sistema las entiende

```python
class BusquedaNatural:
    """Permite buscar noticias con frases naturales en español."""

    def __init__(self, motor_busqueda):
        self.motor = motor_busqueda

    def interpretar_consulta(self, consulta_natural):
        """Interpreta una consulta en lenguaje natural."""
        consulta_natural = consulta_natural.lower()
        filtros = {'sentimiento': None, 'categoria': None}

        if any(p in consulta_natural for p in ['buena', 'positiva', 'optimista']):
            filtros['sentimiento'] = 'positivo'
        elif any(p in consulta_natural for p in ['mala', 'negativa', 'pesimista', 'preocupante']):
            filtros['sentimiento'] = 'negativo'

        categorias_map = {
            'tecnología': 'tecnologia', 'tech': 'tecnologia', 'computación': 'tecnologia',
            'economía': 'economia', 'mercados': 'economia', 'finanzas': 'economia',
            'ciencia': 'ciencia', 'científico': 'ciencia', 'investigación': 'ciencia',
            'gobierno': 'politica', 'política': 'politica',
        }
        for keyword, cat in categorias_map.items():
            if keyword in consulta_natural:
                filtros['categoria'] = cat
                break

        return filtros

    def buscar_natural(self, consulta_natural, top_k=3):
        """Búsqueda que entiende lenguaje natural."""
        filtros = self.interpretar_consulta(consulta_natural)
        resultados = self.motor.buscar_vectorial(consulta_natural, top_k=top_k * 2)

        # Aplicar filtros
        filtrados = []
        for r in resultados:
            if filtros['sentimiento'] and r['sentimiento'] != filtros['sentimiento']:
                continue
            if filtros['categoria'] and r['categoria'] != filtros['categoria']:
                continue
            filtrados.append(r)

        return filtrados[:top_k] if filtrados else resultados[:top_k]


busqueda_nl = BusquedaNatural(motor)

consultas_naturales = [
    "Muéstrame noticias positivas sobre tecnología",
    "¿Qué noticias hay sobre datos del gobierno?",
    "Busco información preocupante sobre el clima",
    "¿Hay algo nuevo de programación en Python?",
]

print("=== FASE 4.3: Búsqueda en Lenguaje Natural ===\n")
for consulta in consultas_naturales:
    resultados = busqueda_nl.buscar_natural(consulta, top_k=2)
    print(f"  Usuario: \"{consulta}\"")
    if resultados:
        for r in resultados:
            print(f"    → [{r['relevancia']:.3f}] {r['titulo'][:50]}...")
    else:
        print(f"    → Sin resultados relevantes")
    print()
```

## Fase 5: Chatbot y Sistema Question/Answering

El alumno integra un chatbot que responde preguntas sobre las noticias procesadas por el sistema, combinando recuperación de información con generación de respuestas.

### 5.1 Chatbot basado en similitud

```python
class ChatbotSIMANW:
    """
    Chatbot del SIMANW que responde preguntas sobre las noticias
    procesadas usando cálculo de similitud.
    """

    def __init__(self, noticias):
        self.noticias = noticias
        self.historial = []
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=2000)
        self._construir_base()

    def _construir_base(self):
        """Construye la base de conocimiento a partir de las noticias."""
        self.pares_qa = []
        for n in self.noticias:
            titulo = n['titulo']
            cuerpo = n['cuerpo']
            cat = n.get('categoria_predicha', n.get('categoria_original', ''))
            sent = n.get('sentimiento', {}).get('etiqueta', '')

            self.pares_qa.append({
                'contexto': f"{titulo} {cuerpo}",
                'respuesta': f"{titulo}. {cuerpo}",
                'tipo': 'contenido'
            })
            self.pares_qa.append({
                'contexto': f"categoría tema tipo {cat} {titulo}",
                'respuesta': f"Esa noticia pertenece a la categoría '{cat}': {titulo}",
                'tipo': 'categoria'
            })
            self.pares_qa.append({
                'contexto': f"sentimiento opinión tono {sent} {titulo}",
                'respuesta': f"El tono de esa noticia es {sent}: {titulo}",
                'tipo': 'sentimiento'
            })

        contextos = [p['contexto'] for p in self.pares_qa]
        self.matriz_qa = self.vectorizer.fit_transform(contextos)

    def responder(self, pregunta, umbral=0.05):
        """Genera respuesta a una pregunta del usuario."""
        pregunta_vec = self.vectorizer.transform([pregunta])
        similitudes = cosine_similarity(pregunta_vec, self.matriz_qa)[0]
        mejor_idx = similitudes.argmax()
        confianza = similitudes[mejor_idx]

        self.historial.append({'pregunta': pregunta, 'confianza': confianza})

        if confianza < umbral:
            return "No tengo información suficiente para responder eso. ¿Puedes reformular tu pregunta?", 0.0

        return self.pares_qa[mejor_idx]['respuesta'], confianza

    def resumen_interaccion(self):
        n = len(self.historial)
        if n == 0:
            return "Sin interacciones"
        avg = sum(h['confianza'] for h in self.historial) / n
        return f"{n} preguntas, confianza promedio: {avg:.3f}"


chatbot = ChatbotSIMANW(noticias)

print("=== FASE 5.1: Chatbot del SIMANW ===\n")
preguntas_usuario = [
    "¿Qué noticias hay sobre inteligencia artificial?",
    "¿Cuál es el tono de la noticia de los mercados financieros?",
    "¿Hay algo sobre datos abiertos del gobierno?",
    "¿Qué noticias de tecnología tienen sentimiento positivo?",
    "¿Cuál es la capital de Francia?",
]

for pregunta in preguntas_usuario:
    respuesta, confianza = chatbot.responder(pregunta)
    print(f"  Usuario: {pregunta}")
    print(f"  Bot [{confianza:.3f}]: {respuesta[:100]}...")
    print()

print(f"Resumen: {chatbot.resumen_interaccion()}")
```

### 5.2 Sistema Question/Answering completo

El sistema Q&A combina recuperación de información con comprensión de preguntas para dar respuestas precisas.

```python
import re

class SistemaQA:
    """
    Sistema de pregunta-respuesta que comprende la intención del usuario
    y genera respuestas a partir de la información indexada.
    """

    def __init__(self, noticias, motor_busqueda):
        self.noticias = noticias
        self.motor = motor_busqueda
        self.historial_conversacion = []

    def clasificar_intencion(self, pregunta):
        """Determina qué tipo de información busca el usuario."""
        pregunta_lower = pregunta.lower()
        if any(w in pregunta_lower for w in ['cuántas', 'cuantas', 'total', 'número']):
            return 'conteo'
        elif any(w in pregunta_lower for w in ['resumen', 'resume', 'sintetiza']):
            return 'resumen'
        elif any(w in pregunta_lower for w in ['sentimiento', 'tono', 'opinión', 'positiv', 'negativ']):
            return 'sentimiento'
        elif any(w in pregunta_lower for w in ['categoría', 'tema', 'tipo', 'clasifica']):
            return 'categoria'
        elif any(w in pregunta_lower for w in ['compara', 'diferencia', 'relación']):
            return 'comparacion'
        elif any(w in pregunta_lower for w in ['recomienda', 'sugiere', 'similar']):
            return 'recomendacion'
        else:
            return 'busqueda'

    def generar_respuesta(self, pregunta):
        """Genera una respuesta inteligente según la intención."""
        intencion = self.clasificar_intencion(pregunta)

        if intencion == 'conteo':
            return self._respuesta_conteo(pregunta)
        elif intencion == 'sentimiento':
            return self._respuesta_sentimiento(pregunta)
        elif intencion == 'categoria':
            return self._respuesta_categoria(pregunta)
        elif intencion == 'resumen':
            return self._respuesta_resumen()
        elif intencion == 'recomendacion':
            return self._respuesta_recomendacion(pregunta)
        else:
            return self._respuesta_busqueda(pregunta)

    def _respuesta_conteo(self, pregunta):
        cats = Counter(n.get('categoria_predicha', n['categoria_original']) for n in self.noticias)
        resp = f"Tengo {len(self.noticias)} noticias indexadas. "
        resp += "Distribución: " + ", ".join(f"{c}: {n}" for c, n in cats.most_common())
        return resp, 'conteo', 1.0

    def _respuesta_sentimiento(self, pregunta):
        sentimientos = Counter(n['sentimiento']['etiqueta'] for n in self.noticias if 'sentimiento' in n)
        promedio = sum(n['sentimiento']['compound'] for n in self.noticias if 'sentimiento' in n) / len(self.noticias)
        resp = f"Análisis de sentimiento: {dict(sentimientos)}. "
        resp += f"El tono general es {'positivo' if promedio > 0 else 'negativo'} (promedio: {promedio:+.3f})."
        return resp, 'sentimiento', 0.9

    def _respuesta_categoria(self, pregunta):
        cats = Counter(n.get('categoria_predicha', n['categoria_original']) for n in self.noticias)
        resp = "Categorías detectadas en las noticias:\n"
        for cat, count in cats.most_common():
            ejemplos = [n['titulo'][:40] for n in self.noticias
                       if n.get('categoria_predicha', n['categoria_original']) == cat]
            resp += f"  - {cat} ({count}): {ejemplos[0]}...\n"
        return resp, 'categoria', 0.9

    def _respuesta_resumen(self):
        resp = f"Resumen del corpus ({len(self.noticias)} noticias):\n"
        for n in self.noticias:
            sent = n.get('sentimiento', {}).get('etiqueta', '?')
            cat = n.get('categoria_predicha', n['categoria_original'])
            resp += f"  - [{cat}][{sent}] {n['titulo'][:50]}\n"
        return resp, 'resumen', 1.0

    def _respuesta_recomendacion(self, pregunta):
        resultados = self.motor.buscar_vectorial(pregunta, top_k=3)
        if resultados:
            resp = "Te recomiendo estas noticias relacionadas:\n"
            for r in resultados:
                resp += f"  - [{r['relevancia']:.2f}] {r['titulo'][:50]}...\n"
            return resp, 'recomendacion', resultados[0]['relevancia']
        return "No encontré noticias para recomendar sobre ese tema.", 'recomendacion', 0.0

    def _respuesta_busqueda(self, pregunta):
        resultados = self.motor.buscar_vectorial(pregunta, top_k=2)
        if resultados:
            mejor = resultados[0]
            resp = f"{mejor['titulo']}.\n{mejor['snippet']}"
            return resp, 'busqueda', mejor['relevancia']
        return "No encontré información relevante para tu pregunta.", 'busqueda', 0.0

    def conversar(self, pregunta):
        """Interfaz conversacional con historial."""
        respuesta, tipo, confianza = self.generar_respuesta(pregunta)
        self.historial_conversacion.append({
            'pregunta': pregunta,
            'tipo': tipo,
            'confianza': confianza
        })
        return respuesta, tipo, confianza


qa_system = SistemaQA(noticias, motor)

print("=== FASE 5.2: Sistema Question/Answering ===\n")
preguntas_qa = [
    "¿Cuántas noticias tienes?",
    "¿Cuál es el sentimiento general de las noticias?",
    "¿Qué categorías de noticias hay?",
    "Dame un resumen de las noticias",
    "Recomiéndame algo sobre tecnología",
    "¿Qué dice la noticia sobre Python?",
]

for pregunta in preguntas_qa:
    respuesta, tipo, confianza = qa_system.conversar(pregunta)
    print(f"  Pregunta: {pregunta}")
    print(f"  [{tipo}][{confianza:.2f}] {respuesta[:120]}")
    print()
```

## Fase 6: Knowledge Graph y Web Semántica
Todo lo que el SIMANW ha procesado se almacena en un Knowledge Graph semántico. Esto permite consultas SPARQL avanzadas y conectar los datos con fuentes externas de datos abiertos.

### 6.1 Construcción del Knowledge Graph

```python
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF, DCTERMS

class KnowledgeGraphSIMANW:
    """Knowledge Graph semántico del sistema SIMANW."""

    def __init__(self):
        self.graph = Graph()
        self.NS = Namespace("http://simanw.org/ontology/")
        self.DATA = Namespace("http://simanw.org/data/")
        self.graph.bind("simanw", self.NS)
        self.graph.bind("data", self.DATA)
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)
        self._definir_ontologia()

    def _definir_ontologia(self):
        """Define la ontología del SIMANW."""
        # Clases
        self.graph.add((self.NS.Noticia, RDF.type, OWL.Class))
        self.graph.add((self.NS.Autor, RDF.type, OWL.Class))
        self.graph.add((self.NS.Categoria, RDF.type, OWL.Class))
        self.graph.add((self.NS.Fuente, RDF.type, OWL.Class))

        # Propiedades de objeto
        self.graph.add((self.NS.tieneAutor, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.tieneAutor, RDFS.domain, self.NS.Noticia))
        self.graph.add((self.NS.tieneAutor, RDFS.range, self.NS.Autor))
        self.graph.add((self.NS.tieneCategoria, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.provieneDe, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.relacionadaCon, RDF.type, OWL.ObjectProperty))

        # Propiedades de datos
        self.graph.add((self.NS.sentimientoScore, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.sentimientoEtiqueta, RDF.type, OWL.DatatypeProperty))

    def agregar_noticia(self, noticia, noticia_id):
        """Agrega una noticia procesada al knowledge graph."""
        uri = self.DATA[f"noticia_{noticia_id}"]
        self.graph.add((uri, RDF.type, self.NS.Noticia))
        self.graph.add((uri, DC.title, Literal(noticia['titulo'], lang="es")))
        self.graph.add((uri, DC.description, Literal(noticia['cuerpo'][:200], lang="es")))
        self.graph.add((uri, DC.date, Literal(noticia['fecha'], datatype=XSD.date)))

        # Autor
        autor_uri = self.DATA[f"autor_{noticia['autor'].replace(' ', '_')}"]
        self.graph.add((autor_uri, RDF.type, self.NS.Autor))
        self.graph.add((autor_uri, FOAF.name, Literal(noticia['autor'])))
        self.graph.add((uri, self.NS.tieneAutor, autor_uri))

        # Categoría
        cat = noticia.get('categoria_predicha', noticia.get('categoria_original', 'general'))
        cat_uri = self.DATA[f"categoria_{cat}"]
        self.graph.add((cat_uri, RDF.type, self.NS.Categoria))
        self.graph.add((cat_uri, RDFS.label, Literal(cat, lang="es")))
        self.graph.add((uri, self.NS.tieneCategoria, cat_uri))

        # Sentimiento
        if 'sentimiento' in noticia:
            sent = noticia['sentimiento']
            self.graph.add((uri, self.NS.sentimientoScore,
                           Literal(sent['compound'], datatype=XSD.float)))
            self.graph.add((uri, self.NS.sentimientoEtiqueta,
                           Literal(sent['etiqueta'])))

        # URL fuente
        if 'url' in noticia:
            self.graph.add((uri, self.NS.urlOriginal, Literal(noticia['url'], datatype=XSD.anyURI)))

    def consultar(self, sparql_query):
        """Ejecuta una consulta SPARQL."""
        return list(self.graph.query(sparql_query))

    def total_triples(self):
        return len(self.graph)

    def serializar(self, formato='turtle'):
        return self.graph.serialize(format=formato)


# Construir el Knowledge Graph con las noticias procesadas
kg = KnowledgeGraphSIMANW()
for i, noticia in enumerate(noticias):
    kg.agregar_noticia(noticia, i+1)

print("=== FASE 6.1: Knowledge Graph ===\n")
print(f"Knowledge Graph construido:")
print(f"  Total de triples: {kg.total_triples()}")
print(f"  Noticias almacenadas: {len(noticias)}")

print(f"\nOntología (fragmento en Turtle):")
turtle = kg.serializar('turtle')
lineas = [l for l in turtle.split('\n') if l.strip()][:25]
for l in lineas:
    print(f"  {l}")
```

### 6.2 Consultas SPARQL sobre el Knowledge Graph

```python
print("=== FASE 6.2: Consultas SPARQL ===\n")

# Consulta 1: Todas las noticias con autor y categoría
query1 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX data: <http://simanw.org/data/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?titulo ?autor ?categoria ?fecha
WHERE {
    ?noticia a simanw:Noticia ;
             dc:title ?titulo ;
             dc:date ?fecha ;
             simanw:tieneAutor ?autorURI ;
             simanw:tieneCategoria ?catURI .
    ?autorURI foaf:name ?autor .
    ?catURI rdfs:label ?categoria .
}
ORDER BY DESC(?fecha)
"""
print("Consulta 1: Noticias con metadatos")
print("─" * 60)
for row in kg.consultar(query1):
    print(f"  [{row.fecha}] [{row.categoria}] {str(row.titulo)[:45]}... - {row.autor}")

# Consulta 2: Noticias con sentimiento negativo
query2 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?titulo ?score ?etiqueta
WHERE {
    ?noticia a simanw:Noticia ;
             dc:title ?titulo ;
             simanw:sentimientoScore ?score ;
             simanw:sentimientoEtiqueta ?etiqueta .
    FILTER(?score < -0.05)
}
ORDER BY ?score
"""
print("\n\nConsulta 2: Noticias con sentimiento negativo")
print("─" * 60)
for row in kg.consultar(query2):
    print(f"  [{float(row.score):+.3f}] {str(row.titulo)[:55]}")

# Consulta 3: Conteo por categoría
query3 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?categoria (COUNT(?noticia) as ?total)
WHERE {
    ?noticia a simanw:Noticia ;
             simanw:tieneCategoria ?catURI .
    ?catURI rdfs:label ?categoria .
}
GROUP BY ?categoria
ORDER BY DESC(?total)
"""
print("\n\nConsulta 3: Distribución por categoría")
print("─" * 60)
for row in kg.consultar(query3):
    print(f"  {row.categoria}: {row.total} noticia(s)")

# Consulta 4: Autores y sus noticias
query4 = """
PREFIX simanw: <http://simanw.org/ontology/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?autor (COUNT(?n) as ?publicaciones) (GROUP_CONCAT(?titulo; separator="; ") as ?titulos)
WHERE {
    ?n a simanw:Noticia ;
       dc:title ?titulo ;
       simanw:tieneAutor ?a .
    ?a foaf:name ?autor .
}
GROUP BY ?autor
"""
print("\n\nConsulta 4: Productividad por autor")
print("─" * 60)
for row in kg.consultar(query4):
    print(f"  {row.autor}: {row.publicaciones} publicación(es)")
```

### 6.3 Datos abiertos y conexión con fuentes externas

El SIMANW se conecta con datos abiertos gubernamentales, enriqueciendo la información con datos públicos en formato semántico.

```python
import json

class ConectorDatosAbiertos:
    """Conecta el SIMANW con fuentes de datos abiertos."""

    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.DCAT = Namespace("http://www.w3.org/ns/dcat#")
        self.GOB = Namespace("http://datos.gob.mx/")
        self.kg.graph.bind("dcat", self.DCAT)
        self.kg.graph.bind("gob", self.GOB)

    def cargar_dataset_gobierno(self, nombre, datos, publicador, tema):
        """Integra un dataset de datos abiertos al knowledge graph."""
        ds_uri = self.GOB[f"dataset/{nombre.replace(' ', '_')}"]
        self.kg.graph.add((ds_uri, RDF.type, self.DCAT.Dataset))
        self.kg.graph.add((ds_uri, DC.title, Literal(nombre, lang="es")))
        self.kg.graph.add((ds_uri, DC.publisher, Literal(publicador)))
        self.kg.graph.add((ds_uri, self.GOB.tema, Literal(tema)))

        for i, registro in enumerate(datos):
            reg_uri = self.GOB[f"registro/{nombre.replace(' ', '_')}_{i}"]
            self.kg.graph.add((ds_uri, self.GOB.tieneRegistro, reg_uri))
            for campo, valor in registro.items():
                if isinstance(valor, (int, float)):
                    self.kg.graph.add((reg_uri, self.GOB[campo],
                                     Literal(valor, datatype=XSD.float)))
                else:
                    self.kg.graph.add((reg_uri, self.GOB[campo], Literal(valor, lang="es")))

    def consultar_datos(self, tema=None):
        """Consulta los datos abiertos cargados."""
        filtro = f'FILTER(?tema = "{tema}")' if tema else ''
        query = f"""
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX gob: <http://datos.gob.mx/>

        SELECT ?titulo ?publicador ?tema
        WHERE {{
            ?ds a dcat:Dataset ;
                dc:title ?titulo ;
                dc:publisher ?publicador ;
                gob:tema ?tema .
            {filtro}
        }}
        """
        return list(self.kg.graph.query(query))

    def enlazar_noticias_con_datos(self):
        """Enlaza noticias con datasets relacionados semánticamente."""
        query = """
        PREFIX simanw: <http://simanw.org/ontology/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX gob: <http://datos.gob.mx/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?noticia_titulo ?dataset_titulo ?tema
        WHERE {
            ?noticia a simanw:Noticia ;
                     dc:title ?noticia_titulo ;
                     simanw:tieneCategoria ?cat .
            ?cat rdfs:label ?cat_label .
            ?ds a dcat:Dataset ;
                dc:title ?dataset_titulo ;
                gob:tema ?tema .
            FILTER(CONTAINS(LCASE(?tema), LCASE(?cat_label)))
        }
        """
        return list(self.kg.graph.query(query))


# Integrar datos abiertos
conector = ConectorDatosAbiertos(kg)

conector.cargar_dataset_gobierno(
    "Presupuesto TIC Federal 2026",
    [
        {"dependencia": "SEP", "monto_mdp": 12500, "concepto": "Infraestructura digital educativa"},
        {"dependencia": "SALUD", "monto_mdp": 8900, "concepto": "Expediente clínico electrónico"},
        {"dependencia": "SAT", "monto_mdp": 15600, "concepto": "Plataformas de recaudación"},
    ],
    publicador="Secretaría de Hacienda",
    tema="tecnologia"
)

conector.cargar_dataset_gobierno(
    "Indicadores Económicos Mayo 2026",
    [
        {"indicador": "Inflación anual", "valor": 4.2, "unidad": "porcentaje"},
        {"indicador": "Tipo de cambio", "valor": 18.5, "unidad": "pesos por dólar"},
        {"indicador": "Tasa de desempleo", "valor": 3.1, "unidad": "porcentaje"},
    ],
    publicador="INEGI / Banco de México",
    tema="economia"
)

conector.cargar_dataset_gobierno(
    "Emisiones CO2 por Sector 2025",
    [
        {"sector": "Energía", "emisiones_mtco2": 450, "variacion": -2.1},
        {"sector": "Transporte", "emisiones_mtco2": 180, "variacion": 1.5},
        {"sector": "Industria", "emisiones_mtco2": 120, "variacion": -3.8},
    ],
    publicador="SEMARNAT",
    tema="ciencia"
)

print("=== FASE 6.3: Datos Abiertos Integrados ===\n")
print(f"Triples totales en KG (con datos abiertos): {kg.total_triples()}")

print("\nDatasets de datos abiertos cargados:")
for row in conector.consultar_datos():
    print(f"  [{row.tema}] {row.titulo} - {row.publicador}")

print("\nEnlaces noticias ↔ datos abiertos:")
enlaces = conector.enlazar_noticias_con_datos()
if enlaces:
    for row in enlaces:
        print(f"  Noticia: {str(row.noticia_titulo)[:40]}...")
        print(f"  Dataset: {row.dataset_titulo}")
        print()
else:
    print("  (Los enlaces se generan cuando las categorías coinciden con los temas)")
```

### 6.4 Consulta a endpoints SPARQL externos

```python
from SPARQLWrapper import SPARQLWrapper, JSON

print("=== FASE 6.4: Endpoints SPARQL Externos ===\n")

# Ejemplo de consulta a Wikidata (requiere internet)
query_wikidata = """
SELECT ?item ?itemLabel ?description WHERE {
  ?item wdt:P31 wd:Q7397;      # instancia de: software
        wdt:P277 wd:Q28865;    # lenguaje de programación: Python
        wdt:P366 wd:Q11660.    # uso: inteligencia artificial
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
}
LIMIT 10
"""

print("Consulta para Wikidata (software de IA en Python):")
print(query_wikidata)

# Ejemplo de consulta a DBpedia
query_dbpedia = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?nombre ?descripcion WHERE {
  ?s dbo:genre dbr:Natural_language_processing ;
     rdfs:label ?nombre ;
     rdfs:comment ?descripcion .
  FILTER(LANG(?nombre) = 'es')
  FILTER(LANG(?descripcion) = 'es')
}
LIMIT 5
"""

print("\nConsulta para DBpedia (herramientas NLP):")
print(query_dbpedia)

print("""
Endpoints SPARQL disponibles para el SIMANW:
  - Wikidata:  https://query.wikidata.org/sparql
  - DBpedia:   http://dbpedia.org/sparql
  - datos.gob: Portal de datos abiertos de México

# Código para ejecutar (requiere internet):
# sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
# sparql.setQuery(query_wikidata)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
""")
```

## Fase 7: Reportes Automáticos y Entrega Final

El sistema genera reportes completos automáticamente a partir de toda la información procesada y almacenada.

### 7.1 Generador de reportes

```python
from datetime import datetime
from collections import Counter

class GeneradorReportes:
    """Genera reportes automáticos del SIMANW."""

    def __init__(self, noticias, knowledge_graph):
        self.noticias = noticias
        self.kg = knowledge_graph

    def reporte_completo(self):
        """Genera el reporte integrador completo."""
        lineas = []
        lineas.append("=" * 70)
        lineas.append("  REPORTE AUTOMÁTICO - SISTEMA SIMANW")
        lineas.append(f"  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lineas.append("=" * 70)

        # Sección 1: Resumen ejecutivo
        lineas.append("\n1. RESUMEN EJECUTIVO")
        lineas.append("─" * 40)
        lineas.append(f"   Noticias procesadas: {len(self.noticias)}")
        lineas.append(f"   Triples en Knowledge Graph: {self.kg.total_triples()}")

        cats = Counter(n.get('categoria_predicha', n['categoria_original']) for n in self.noticias)
        lineas.append(f"   Categorías detectadas: {len(cats)}")

        sents = [n['sentimiento']['compound'] for n in self.noticias if 'sentimiento' in n]
        promedio = sum(sents) / len(sents) if sents else 0
        lineas.append(f"   Sentimiento promedio: {promedio:+.3f}")
        lineas.append(f"   Tono general: {'POSITIVO' if promedio > 0.05 else 'NEGATIVO' if promedio < -0.05 else 'NEUTRAL'}")

        # Sección 2: Distribución por categoría
        lineas.append("\n2. DISTRIBUCIÓN POR CATEGORÍA")
        lineas.append("─" * 40)
        for cat, count in cats.most_common():
            barra = "█" * (count * 8)
            pct = 100 * count / len(self.noticias)
            lineas.append(f"   {cat:<12} {barra} {count} ({pct:.0f}%)")

        # Sección 3: Análisis de sentimiento
        lineas.append("\n3. ANÁLISIS DE SENTIMIENTO")
        lineas.append("─" * 40)
        sent_dist = Counter(n['sentimiento']['etiqueta'] for n in self.noticias if 'sentimiento' in n)
        for etiqueta, count in sent_dist.most_common():
            emoji = "+" if etiqueta == 'positivo' else "-" if etiqueta == 'negativo' else "~"
            lineas.append(f"   [{emoji}] {etiqueta}: {count} noticia(s)")

        lineas.append("\n   Detalle por noticia:")
        for n in sorted(self.noticias, key=lambda x: x.get('sentimiento', {}).get('compound', 0)):
            if 'sentimiento' in n:
                s = n['sentimiento']
                lineas.append(f"   [{s['compound']:+.3f}] {n['titulo'][:50]}")

        # Sección 4: Noticias procesadas
        lineas.append("\n4. CATÁLOGO DE NOTICIAS")
        lineas.append("─" * 40)
        for i, n in enumerate(self.noticias, 1):
            cat = n.get('categoria_predicha', n['categoria_original'])
            sent = n.get('sentimiento', {}).get('etiqueta', '?')
            lineas.append(f"   {i}. [{n['fecha']}] [{cat}] [{sent}]")
            lineas.append(f"      {n['titulo']}")
            lineas.append(f"      Autor: {n['autor']} | Fuente: {n['fuente']}")
            lineas.append("")

        # Sección 5: Capacidades del sistema
        lineas.append("\n5. CAPACIDADES DEMOSTRADAS")
        lineas.append("─" * 40)
        capacidades = [
            ("Rastreo Web", "Extracción automática con BeautifulSoup/Scrapy"),
            ("NLP", "Tokenización, stemming, stopwords, representación TF-IDF"),
            ("Clasificación", "Categorización automática con SVM/NB"),
            ("Sentimientos", "Análisis de polaridad con VADER"),
            ("Recomendación", "Sugerencias basadas en similitud coseno"),
            ("Publicidad", "Detección de temas en conversación"),
            ("Búsqueda", "Motor con índice invertido y ranking vectorial"),
            ("Evaluación IRS", "Precision, Recall, F1, MAP, P@K"),
            ("Chatbot", "Respuestas por similitud semántica"),
            ("Q&A", "Pregunta-respuesta con comprensión de intención"),
            ("Knowledge Graph", "Ontología OWL + triples RDF"),
            ("SPARQL", "Consultas semánticas sobre el grafo"),
            ("Datos Abiertos", "Integración con datasets gubernamentales"),
            ("Reportes", "Generación automática de resúmenes"),
        ]
        for nombre, desc in capacidades:
            lineas.append(f"   [OK] {nombre:<16} → {desc}")

        lineas.append("\n" + "=" * 70)
        lineas.append("  FIN DEL REPORTE")
        lineas.append("=" * 70)

        return "\n".join(lineas)


reportero = GeneradorReportes(noticias, kg)
print(reportero.reporte_completo())
```

### 7.2 Integración final: Pipeline completo

```python
print("""
╔══════════════════════════════════════════════════════════════════════╗
║           SISTEMA SIMANW - PIPELINE COMPLETO                         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Fase 1: RASTREO WEB                                                 ║
║    → HTML parsing (BeautifulSoup)                                    ║
║    → Control de alcance (dominio/directorio)                         ║
║    → Spider (Scrapy en producción)                                   ║
║    → Almacenamiento (JSON/CSV)                                       ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 2: PROCESAMIENTO NLP                                           ║
║    → Tokenización + Limpieza                                         ║
║    → Stopwords + Stemming                                            ║
║    → Vectorización TF-IDF                                            ║
║    → Cálculo de similitudes (coseno)                                 ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 3: ANÁLISIS AUTOMÁTICO                                         ║
║    → Clasificación (SVM/NB)                                          ║
║    → Sentimiento (VADER)                                             ║
║    → Recomendación (similitud contenido)                             ║
║    → Detección temas + publicidad                                    ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 4: MOTOR DE BÚSQUEDA                                           ║
║    → Índice invertido                                                ║
║    → Búsqueda booleana y vectorial                                   ║
║    → Evaluación (P, R, F1, MAP)                                      ║
║    → Búsqueda en lenguaje natural                                    ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 5: CHATBOT + Q&A                                               ║
║    → Chatbot por similitud                                           ║
║    → Sistema pregunta-respuesta                                      ║
║    → Comprensión de intención                                        ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 6: WEB SEMÁNTICA                                               ║
║    → Ontología OWL del dominio                                       ║
║    → Knowledge Graph (RDF triples)                                   ║
║    → Consultas SPARQL                                                ║
║    → Datos abiertos + Linked Data                                    ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 7: REPORTES + ENTREGA                                          ║
║    → Generación automática de reportes                               ║
║    → Estadísticas y visualización                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")
```

## Actividades Complementarias

Las siguientes actividades deben integrarse al proyecto SIMANW para reforzar y extender cada fase. Cada actividad tiene complejidad media: requiere investigación y programación adicional, pero se apoya en lo ya construido.

### AC-1: Rastreo de un sitio real con paginación (Fase 1)

El alumno debe adaptar el extractor para rastrear un portal de noticias real (por ejemplo, un periódico local o un blog tecnológico) que tenga paginación. Debe:

- Respetar el archivo robots.txt del sitio
- Implementar un delay entre peticiones (mínimo 3 segundos)
- Navegar automáticamente a las siguientes páginas (paginación)
- Extraer al menos 20 noticias reales
- Almacenar los resultados en un archivo JSON

```python
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class RastreadorPaginado:
    """
    AC-1: Rastreador que navega paginación de un sitio real.
    El alumno debe adaptarlo a un portal específico.
    """

    def __init__(self, url_base, selector_articulos, selector_siguiente,
                 delay=3, max_paginas=5):
        self.url_base = url_base
        self.selector_articulos = selector_articulos
        self.selector_siguiente = selector_siguiente
        self.delay = delay
        self.max_paginas = max_paginas
        self.resultados = []

    def extraer_pagina(self, html, url_actual):
        """El alumno implementa la extracción según el sitio elegido."""
        soup = BeautifulSoup(html, 'html.parser')
        articulos = soup.select(self.selector_articulos)
        noticias_pagina = []
        for art in articulos:
            titulo_elem = art.find(['h2', 'h3', 'h1'])
            parrafo_elem = art.find('p')
            enlace_elem = art.find('a')
            if titulo_elem:
                noticias_pagina.append({
                    'titulo': titulo_elem.get_text(strip=True),
                    'resumen': parrafo_elem.get_text(strip=True) if parrafo_elem else '',
                    'url': urljoin(url_actual, enlace_elem['href']) if enlace_elem and enlace_elem.get('href') else '',
                })
        return noticias_pagina

    def obtener_siguiente_pagina(self, html, url_actual):
        """Encuentra el enlace a la siguiente página."""
        soup = BeautifulSoup(html, 'html.parser')
        siguiente = soup.select_one(self.selector_siguiente)
        if siguiente and siguiente.get('href'):
            return urljoin(url_actual, siguiente['href'])
        return None

    def rastrear(self):
        """Ejecuta el rastreo completo con paginación."""
        url_actual = self.url_base
        paginas_visitadas = 0

        while url_actual and paginas_visitadas < self.max_paginas:
            print(f"  Rastreando página {paginas_visitadas + 1}: {url_actual[:60]}...")

            # En producción: response = requests.get(url_actual)
            # Aquí simulamos para no depender de conexión
            html_simulado = f"""
            <div class="articulos">
              <article><h2>Noticia {paginas_visitadas*3 + 1} de ejemplo</h2>
              <p>Contenido de la noticia extraída del sitio real.</p>
              <a href="/noticia/{paginas_visitadas*3 + 1}">Leer</a></article>
              <article><h2>Noticia {paginas_visitadas*3 + 2} de ejemplo</h2>
              <p>Otra noticia con información relevante.</p>
              <a href="/noticia/{paginas_visitadas*3 + 2}">Leer</a></article>
              <article><h2>Noticia {paginas_visitadas*3 + 3} de ejemplo</h2>
              <p>Tercera noticia de esta página.</p>
              <a href="/noticia/{paginas_visitadas*3 + 3}">Leer</a></article>
            </div>
            <a class="next-page" href="/noticias?page={paginas_visitadas+2}">Siguiente</a>
            """

            noticias = self.extraer_pagina(html_simulado, url_actual)
            self.resultados.extend(noticias)

            url_siguiente = self.obtener_siguiente_pagina(html_simulado, url_actual)
            paginas_visitadas += 1

            if paginas_visitadas < self.max_paginas and url_siguiente:
                url_actual = url_siguiente
                time.sleep(0.1)  # En producción: time.sleep(self.delay)
            else:
                break

        return self.resultados

    def guardar_json(self, archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)
        return len(self.resultados)


# Demostración
rastreador_paginado = RastreadorPaginado(
    url_base="https://ejemplo-noticias.com/ultimas",
    selector_articulos="article",
    selector_siguiente="a.next-page",
    delay=3,
    max_paginas=4
)

print("=== AC-1: Rastreo con Paginación ===\n")
resultados = rastreador_paginado.rastrear()
print(f"\nTotal noticias extraídas: {len(resultados)}")
print(f"Primeras 5:")
for r in resultados[:5]:
    print(f"  - {r['titulo']}")
```

### AC-2: Nube de palabras y estadísticas de un discurso (Fase 2)

El alumno debe tomar un texto largo (discurso político, artículo científico, o reseña extensa) y generar:

- Frecuencia de bigramas y trigramas (no solo unigramas)
- Análisis de riqueza léxica por secciones del texto
- Identificación de entidades nombradas (personas, lugares, organizaciones)
- Resumen estadístico comparativo si se tienen múltiples textos

```python
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import bigrams, trigrams
from collections import Counter
import re

class AnalisisDiscurso:
    """
    AC-2: Análisis estadístico profundo de textos.
    El alumno lo aplica a textos reales (discursos, artículos, etc.)
    """

    def __init__(self, idioma='spanish'):
        self.stop_words = set(stopwords.words(idioma))
        self.idioma = idioma

    def analizar(self, texto, titulo="Documento"):
        """Análisis completo de un texto."""
        oraciones = sent_tokenize(texto, language=self.idioma)
        tokens = word_tokenize(texto.lower(), language=self.idioma)
        tokens_alfa = [t for t in tokens if t.isalpha() and len(t) > 2]
        tokens_filtrados = [t for t in tokens_alfa if t not in self.stop_words]

        # N-gramas
        bigs = list(bigrams(tokens_filtrados))
        trigs = list(trigrams(tokens_filtrados))

        # Riqueza léxica por secciones (dividir en cuartos)
        cuarto = len(tokens_filtrados) // 4
        riqueza_secciones = []
        for i in range(4):
            seccion = tokens_filtrados[i*cuarto:(i+1)*cuarto]
            if seccion:
                rl = len(set(seccion)) / len(seccion)
                riqueza_secciones.append(rl)

        # Entidades (heurística simple: palabras que inician con mayúscula)
        tokens_original = word_tokenize(texto, language=self.idioma)
        posibles_entidades = [t for t in tokens_original
                            if t[0].isupper() and t.isalpha() and len(t) > 2
                            and t.lower() not in self.stop_words]

        return {
            'titulo': titulo,
            'oraciones': len(oraciones),
            'palabras_totales': len(tokens_alfa),
            'vocabulario_unico': len(set(tokens_filtrados)),
            'riqueza_lexica_global': len(set(tokens_filtrados)) / max(len(tokens_filtrados), 1),
            'riqueza_por_seccion': riqueza_secciones,
            'promedio_palabras_oracion': len(tokens_alfa) / max(len(oraciones), 1),
            'top_unigramas': Counter(tokens_filtrados).most_common(10),
            'top_bigramas': Counter(bigs).most_common(7),
            'top_trigramas': Counter(trigs).most_common(5),
            'posibles_entidades': Counter(posibles_entidades).most_common(8),
        }

    def comparar_textos(self, analisis_lista):
        """Compara estadísticas entre múltiples textos."""
        comparativa = []
        for a in analisis_lista:
            comparativa.append({
                'titulo': a['titulo'],
                'palabras': a['palabras_totales'],
                'vocabulario': a['vocabulario_unico'],
                'riqueza': a['riqueza_lexica_global'],
                'promedio_oracion': a['promedio_palabras_oracion']
            })
        return comparativa


analizador_disc = AnalisisDiscurso()

texto_discurso = """La educación es la herramienta más poderosa para transformar
una sociedad. En México, la inversión en educación debe ser prioritaria para
garantizar el desarrollo económico y social. Los jóvenes mexicanos merecen
oportunidades de calidad en todos los niveles educativos. Las universidades
tecnológicas y los institutos de investigación son pilares fundamentales para
la innovación. La ciencia y la tecnología son motores del progreso nacional.
El Instituto Tecnológico de Morelia ha formado generaciones de ingenieros que
contribuyen al desarrollo del país. La inteligencia artificial y la programación
son competencias esenciales para el futuro laboral. México necesita más
profesionales en ciencias computacionales y recuperación de información."""

texto_cientifico = """El procesamiento de lenguaje natural permite a las computadoras
comprender y generar texto humano. Los modelos de aprendizaje profundo como BERT
y GPT han revolucionado este campo. La representación vectorial de documentos
mediante TF-IDF sigue siendo fundamental para sistemas de recuperación de información.
Los algoritmos de clasificación como Naive Bayes y SVM logran alta precisión en
categorización de texto. El análisis de sentimientos combina técnicas léxicas con
aprendizaje automático para determinar la polaridad emocional de un texto."""

print("=== AC-2: Análisis Estadístico de Discursos ===\n")

analisis1 = analizador_disc.analizar(texto_discurso, "Discurso Educativo")
analisis2 = analizador_disc.analizar(texto_cientifico, "Texto Científico")

for analisis in [analisis1, analisis2]:
    print(f"--- {analisis['titulo']} ---")
    print(f"  Oraciones: {analisis['oraciones']}")
    print(f"  Palabras: {analisis['palabras_totales']}")
    print(f"  Vocabulario: {analisis['vocabulario_unico']}")
    print(f"  Riqueza léxica: {analisis['riqueza_lexica_global']:.3f}")
    print(f"  Prom. palabras/oración: {analisis['promedio_palabras_oracion']:.1f}")
    print(f"  Riqueza por sección: {[f'{r:.3f}' for r in analisis['riqueza_por_seccion']]}")
    print(f"  Top bigramas: {analisis['top_bigramas'][:4]}")
    print(f"  Posibles entidades: {[e[0] for e in analisis['posibles_entidades'][:5]]}")
    print()

print("--- Comparativa ---")
comp = analizador_disc.comparar_textos([analisis1, analisis2])
print(f"{'Texto':<20} {'Palabras':>9} {'Vocab':>7} {'Riqueza':>8} {'P/Oración':>10}")
for c in comp:
    print(f"{c['titulo']:<20} {c['palabras']:>9} {c['vocabulario']:>7} {c['riqueza']:>8.3f} {c['promedio_oracion']:>10.1f}")
```

### AC-3: Clasificador multimodelo con selección automática (Fase 3)

El alumno entrena múltiples clasificadores y el sistema selecciona automáticamente el mejor según los datos, aplicando validación cruzada.

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import numpy as np

class SelectorModelo:
    """
    AC-3: Entrena múltiples modelos y selecciona el mejor automáticamente.
    El alumno debe agregar más datos de entrenamiento de sus noticias reales.
    """

    def __init__(self):
        self.modelos = {
            'Naive Bayes': MultinomialNB(alpha=0.1),
            'SVM Lineal': LinearSVC(max_iter=3000, C=1.0),
            'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        }
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.mejor_modelo = None
        self.resultados = {}

    def evaluar_todos(self, textos, etiquetas, cv_folds=3):
        """Evalúa todos los modelos con validación cruzada."""
        X = self.vectorizer.fit_transform(textos)
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

        for nombre, modelo in self.modelos.items():
            try:
                scores = cross_val_score(modelo, X, etiquetas, cv=cv, scoring='accuracy')
                self.resultados[nombre] = {
                    'accuracy_mean': scores.mean(),
                    'accuracy_std': scores.std(),
                    'scores': scores.tolist()
                }
            except Exception as e:
                self.resultados[nombre] = {'error': str(e)}

        # Seleccionar el mejor
        validos = {k: v for k, v in self.resultados.items() if 'accuracy_mean' in v}
        if validos:
            mejor_nombre = max(validos, key=lambda k: validos[k]['accuracy_mean'])
            self.mejor_modelo = (mejor_nombre, self.modelos[mejor_nombre])
            # Entrenar el mejor con todos los datos
            self.mejor_modelo[1].fit(X, etiquetas)

        return self.resultados

    def predecir(self, textos):
        """Predice usando el mejor modelo seleccionado."""
        if not self.mejor_modelo:
            raise ValueError("Primero ejecuta evaluar_todos()")
        X = self.vectorizer.transform(textos)
        return self.mejor_modelo[1].predict(X)

    def reporte(self):
        """Genera reporte comparativo de modelos."""
        lineas = ["Modelo                  | Accuracy   | Std Dev"]
        lineas.append("-" * 50)
        for nombre, res in sorted(self.resultados.items(),
                                  key=lambda x: x[1].get('accuracy_mean', 0),
                                  reverse=True):
            if 'accuracy_mean' in res:
                marca = " ★" if self.mejor_modelo and nombre == self.mejor_modelo[0] else ""
                lineas.append(f"{nombre:<23} | {res['accuracy_mean']:.4f}     | {res['accuracy_std']:.4f}{marca}")
            else:
                lineas.append(f"{nombre:<23} | ERROR      | {res.get('error', '')[:20]}")
        return "\n".join(lineas)


# Datos expandidos para demostración
textos_ac3 = [
    "inteligencia artificial deep learning redes neuronales transformers",
    "programación software desarrollo aplicaciones web python javascript",
    "startup tecnológica innovación digital plataforma cloud",
    "ciberseguridad hackers vulnerabilidad protección datos privacidad",
    "inflación tasas interés banco central política monetaria",
    "bolsa acciones mercado valores inversión rendimiento portafolio",
    "desempleo recesión económica crisis laboral empleo informal",
    "comercio exportaciones importaciones balanza aranceles tratado",
    "investigación científica laboratorio experimento publicación revista",
    "cambio climático emisiones carbono calentamiento temperatura global",
    "vacuna medicamento ensayo clínico pacientes tratamiento hospital",
    "espacio cohete satélite misión astronauta exploración lunar",
    "elecciones presidente candidato partido campaña votación democracia",
    "congreso legisladores reforma ley aprobación dictamen senado",
    "seguridad policía crimen organizado justicia tribunal sentencia",
    "gobierno programa social presupuesto política pública decreto",
]
etiquetas_ac3 = [
    'tecnologia', 'tecnologia', 'tecnologia', 'tecnologia',
    'economia', 'economia', 'economia', 'economia',
    'ciencia', 'ciencia', 'ciencia', 'ciencia',
    'politica', 'politica', 'politica', 'politica',
]

selector = SelectorModelo()
resultados = selector.evaluar_todos(textos_ac3, etiquetas_ac3, cv_folds=3)

print("=== AC-3: Selección Automática de Modelo ===\n")
print(selector.reporte())
print(f"\nModelo seleccionado: {selector.mejor_modelo[0]}")

# Probar con nuevos textos
nuevos = [
    "nueva aplicación de machine learning para detectar fraudes",
    "el presidente anunció reformas al sistema de justicia",
    "los mercados cerraron con pérdidas por tercer día consecutivo",
]
predicciones = selector.predecir(nuevos)
print(f"\nPredicciones con el mejor modelo:")
for texto, pred in zip(nuevos, predicciones):
    print(f"  [{pred}] {texto[:50]}...")
```

### AC-4: Análisis de hilos de discusión de red social (Fase 3-4)

El alumno rastrea (o simula) un hilo de discusión de una red social, analiza la evolución del sentimiento, detecta los subtemas discutidos y genera un resumen automático del hilo.

```python
from collections import Counter, defaultdict
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import re

class AnalizadorHiloDiscusion:
    """
    AC-4: Analiza un hilo completo de red social.
    El alumno debe aplicarlo a datos reales (Twitter/X, Reddit, foros).
    """

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.mensajes = []

    def cargar_hilo(self, mensajes):
        """Carga un hilo de discusión."""
        self.mensajes = mensajes
        for msg in self.mensajes:
            msg['sentimiento'] = self.sia.polarity_scores(msg['texto'])['compound']

    def evolucion_sentimiento(self, ventana=3):
        """Analiza cómo evoluciona el sentimiento a lo largo del hilo."""
        sentimientos = [m['sentimiento'] for m in self.mensajes]
        evolucion = []
        for i in range(len(sentimientos)):
            inicio = max(0, i - ventana + 1)
            promedio_ventana = sum(sentimientos[inicio:i+1]) / (i - inicio + 1)
            evolucion.append({
                'posicion': i + 1,
                'sentimiento_puntual': sentimientos[i],
                'tendencia': promedio_ventana
            })
        return evolucion

    def detectar_subtemas(self, n_clusters=3):
        """Detecta subtemas en el hilo usando clustering."""
        textos = [m['texto'] for m in self.mensajes]
        vec = TfidfVectorizer(max_features=500, stop_words='english')
        X = vec.fit_transform(textos)

        n_clusters = min(n_clusters, len(textos))
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = km.fit_predict(X)

        subtemas = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            subtemas[cluster_id].append(i)

        # Extraer palabras clave de cada subtema
        terminos = vec.get_feature_names_out()
        subtemas_info = {}
        for cluster_id, indices in subtemas.items():
            centroide = km.cluster_centers_[cluster_id]
            top_idx = centroide.argsort()[-5:][::-1]
            keywords = [terminos[j] for j in top_idx]
            subtemas_info[cluster_id] = {
                'keywords': keywords,
                'n_mensajes': len(indices),
                'mensajes_idx': indices
            }

        return subtemas_info

    def usuarios_mas_activos(self, top_n=5):
        """Identifica usuarios más participativos."""
        participacion = Counter(m['usuario'] for m in self.mensajes)
        return participacion.most_common(top_n)

    def resumen_hilo(self):
        """Genera resumen automático del hilo."""
        total = len(self.mensajes)
        sent_promedio = sum(m['sentimiento'] for m in self.mensajes) / total
        positivos = sum(1 for m in self.mensajes if m['sentimiento'] > 0.05)
        negativos = sum(1 for m in self.mensajes if m['sentimiento'] < -0.05)

        hashtags = Counter()
        for m in self.mensajes:
            tags = re.findall(r'#(\w+)', m['texto'])
            hashtags.update(tags)

        return {
            'total_mensajes': total,
            'participantes': len(set(m['usuario'] for m in self.mensajes)),
            'sentimiento_promedio': sent_promedio,
            'tono': 'positivo' if sent_promedio > 0.05 else 'negativo' if sent_promedio < -0.05 else 'mixto',
            'positivos_pct': 100 * positivos / total,
            'negativos_pct': 100 * negativos / total,
            'hashtags_top': hashtags.most_common(5),
            'usuarios_activos': self.usuarios_mas_activos(3),
        }


# Simular un hilo de discusión sobre IA
hilo_ia = [
    {"usuario": "@dev_laura", "texto": "Just tried the new AI coding assistant and it's amazing! #AI #coding",
     "timestamp": "10:00"},
    {"usuario": "@tech_mike", "texto": "I agree, the code suggestions are incredibly accurate #AI",
     "timestamp": "10:05"},
    {"usuario": "@skeptic_joe", "texto": "But what about job displacement? This AI thing worries me a lot",
     "timestamp": "10:08"},
    {"usuario": "@dev_laura", "texto": "Good point Joe, but I think it's a tool not a replacement #AItools",
     "timestamp": "10:12"},
    {"usuario": "@data_sara", "texto": "The real concern is bias in training data, we need better datasets",
     "timestamp": "10:15"},
    {"usuario": "@tech_mike", "texto": "True, but the progress is undeniable. Exciting times! #innovation",
     "timestamp": "10:20"},
    {"usuario": "@skeptic_joe", "texto": "I lost my freelance gig because of AI. This is terrible for workers",
     "timestamp": "10:25"},
    {"usuario": "@prof_chen", "texto": "Research shows AI creates more jobs than it destroys historically",
     "timestamp": "10:30"},
    {"usuario": "@data_sara", "texto": "We need regulation and ethical guidelines urgently #AIethics",
     "timestamp": "10:35"},
    {"usuario": "@dev_laura", "texto": "Totally agree with Sara. Responsible AI development is key #responsible",
     "timestamp": "10:40"},
    {"usuario": "@tech_mike", "texto": "Companies investing in AI training for employees is the best approach",
     "timestamp": "10:45"},
    {"usuario": "@prof_chen", "texto": "Great discussion everyone! The future needs both innovation and responsibility",
     "timestamp": "10:50"},
]

analizador_hilo = AnalizadorHiloDiscusion()
analizador_hilo.cargar_hilo(hilo_ia)

print("=== AC-4: Análisis de Hilo de Discusión ===\n")

# Resumen
resumen = analizador_hilo.resumen_hilo()
print("--- Resumen del Hilo ---")
print(f"  Mensajes: {resumen['total_mensajes']}")
print(f"  Participantes: {resumen['participantes']}")
print(f"  Tono general: {resumen['tono']} ({resumen['sentimiento_promedio']:+.3f})")
print(f"  Positivos: {resumen['positivos_pct']:.0f}% | Negativos: {resumen['negativos_pct']:.0f}%")
print(f"  Hashtags: {resumen['hashtags_top']}")
print(f"  Más activos: {resumen['usuarios_activos']}")

# Evolución del sentimiento
print("\n--- Evolución del Sentimiento ---")
evolucion = analizador_hilo.evolucion_sentimiento(ventana=3)
for e in evolucion:
    barra = "+" * int(max(0, e['tendencia'] * 10)) + "-" * int(max(0, -e['tendencia'] * 10))
    print(f"  Msg {e['posicion']:>2}: [{e['sentimiento_puntual']:+.2f}] tendencia: {e['tendencia']:+.3f} |{barra}")

# Subtemas
print("\n--- Subtemas Detectados ---")
subtemas = analizador_hilo.detectar_subtemas(n_clusters=3)
for cluster_id, info in subtemas.items():
    print(f"  Subtema {cluster_id+1} ({info['n_mensajes']} msgs): {info['keywords']}")
```

### AC-5: Evaluación comparativa de modelos de búsqueda (Fase 4)

El alumno implementa y compara formalmente el modelo booleano vs. el modelo vectorial usando las mismas consultas y métricas.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ComparadorModelos:
    """
    AC-5: Compara formalmente modelo booleano vs. vectorial.
    El alumno documenta qué modelo funciona mejor y por qué.
    """

    def __init__(self, documentos):
        self.documentos = documentos
        self.textos = [f"{d['titulo']} {d['cuerpo']}" for d in documentos]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matriz = self.vectorizer.fit_transform(self.textos)

        # Índice invertido para modelo booleano
        self.indice = {}
        for i, texto in enumerate(self.textos):
            for palabra in texto.lower().split():
                if palabra not in self.indice:
                    self.indice[palabra] = set()
                self.indice[palabra].add(i)

    def busqueda_booleana(self, consulta):
        """Modelo booleano: AND de todos los términos."""
        terminos = consulta.lower().split()
        if not terminos:
            return []
        resultado = self.indice.get(terminos[0], set()).copy()
        for t in terminos[1:]:
            resultado &= self.indice.get(t, set())
        return sorted(resultado)

    def busqueda_vectorial(self, consulta, top_k=5):
        """Modelo vectorial: ranking por similitud coseno."""
        q_vec = self.vectorizer.transform([consulta])
        sims = cosine_similarity(q_vec, self.matriz)[0]
        indices = sims.argsort()[::-1][:top_k]
        return [(i, sims[i]) for i in indices if sims[i] > 0]

    def evaluar_ambos(self, consulta, relevantes):
        """Evalúa ambos modelos con la misma consulta y juicio de relevancia."""
        # Booleano
        bool_result = self.busqueda_booleana(consulta)
        bool_precision = len(set(bool_result) & set(relevantes)) / max(len(bool_result), 1)
        bool_recall = len(set(bool_result) & set(relevantes)) / max(len(relevantes), 1)

        # Vectorial
        vec_result = [idx for idx, _ in self.busqueda_vectorial(consulta, top_k=len(self.documentos))]
        vec_top_k = vec_result[:len(bool_result)] if bool_result else vec_result[:3]
        vec_precision = len(set(vec_top_k) & set(relevantes)) / max(len(vec_top_k), 1)
        vec_recall = len(set(vec_top_k) & set(relevantes)) / max(len(relevantes), 1)

        return {
            'consulta': consulta,
            'booleano': {
                'recuperados': len(bool_result),
                'precision': bool_precision,
                'recall': bool_recall
            },
            'vectorial': {
                'recuperados': len(vec_top_k),
                'precision': vec_precision,
                'recall': vec_recall
            }
        }


comparador = ComparadorModelos(noticias)

# Consultas de evaluación con juicios de relevancia manuales
consultas_eval = [
    {"consulta": "inteligencia artificial", "relevantes": [0, 3]},
    {"consulta": "mercados volatilidad economía", "relevantes": [1]},
    {"consulta": "datos abiertos gobierno", "relevantes": [4]},
    {"consulta": "cambio climático científico", "relevantes": [2]},
]

print("=== AC-5: Comparación Booleano vs. Vectorial ===\n")
print(f"{'Consulta':<30} | {'Modelo':<10} | {'Recup':>5} | {'Prec':>6} | {'Recall':>6}")
print("─" * 75)

sum_bool_p, sum_vec_p = 0, 0
sum_bool_r, sum_vec_r = 0, 0

for ce in consultas_eval:
    resultado = comparador.evaluar_ambos(ce['consulta'], ce['relevantes'])
    b = resultado['booleano']
    v = resultado['vectorial']
    sum_bool_p += b['precision']
    sum_vec_p += v['precision']
    sum_bool_r += b['recall']
    sum_vec_r += v['recall']
    print(f"{ce['consulta']:<30} | {'Booleano':<10} | {b['recuperados']:>5} | {b['precision']:>6.3f} | {b['recall']:>6.3f}")
    print(f"{'':30} | {'Vectorial':<10} | {v['recuperados']:>5} | {v['precision']:>6.3f} | {v['recall']:>6.3f}")
    print()

n = len(consultas_eval)
print("─" * 75)
print(f"{'PROMEDIO':<30} | {'Booleano':<10} | {'':>5} | {sum_bool_p/n:>6.3f} | {sum_bool_r/n:>6.3f}")
print(f"{'':30} | {'Vectorial':<10} | {'':>5} | {sum_vec_p/n:>6.3f} | {sum_vec_r/n:>6.3f}")
print(f"\nConclusion: El modelo {'vectorial' if sum_vec_p > sum_bool_p else 'booleano'} tiene mejor precision promedio.")
```

### AC-6: Interfaz conversacional con memoria de contexto (Fase 5)

El chatbot debe recordar la conversación anterior y usar ese contexto para mejorar sus respuestas (no responder de forma aislada).

```python
class ChatbotContextual:
    """
    AC-6: Chatbot con memoria de contexto.
    Las respuestas se enriquecen con el historial de la conversación.
    """

    def __init__(self, noticias, motor_busqueda):
        self.noticias = noticias
        self.motor = motor_busqueda
        self.historial = []
        self.contexto_temas = Counter()
        self.usuario_preferencias = {}

    def actualizar_contexto(self, pregunta, respuesta_tipo):
        """Actualiza el contexto basándose en la interacción."""
        self.historial.append({'pregunta': pregunta, 'tipo': respuesta_tipo})
        palabras_clave = pregunta.lower().split()
        for p in palabras_clave:
            if p in ['tecnología', 'ia', 'python', 'programación', 'software']:
                self.contexto_temas['tecnologia'] += 1
            elif p in ['economía', 'mercado', 'finanzas', 'dinero']:
                self.contexto_temas['economia'] += 1
            elif p in ['ciencia', 'clima', 'investigación']:
                self.contexto_temas['ciencia'] += 1

    def responder(self, pregunta):
        """Genera respuesta considerando el contexto previo."""
        pregunta_lower = pregunta.lower()

        # Detectar referencias al contexto
        if any(ref in pregunta_lower for ref in ['eso', 'esa', 'anterior', 'más sobre', 'otra']):
            if self.historial:
                ultimo = self.historial[-1]
                pregunta_expandida = f"{ultimo['pregunta']} {pregunta}"
                resultados = self.motor.buscar_vectorial(pregunta_expandida, top_k=2)
                if resultados:
                    tipo = 'contextual'
                    resp = f"Basándome en nuestra conversación anterior, encontré: {resultados[0]['titulo']}"
                    self.actualizar_contexto(pregunta, tipo)
                    return resp, tipo, resultados[0]['relevancia']

        # Respuesta con sesgo hacia temas de interés del usuario
        resultados = self.motor.buscar_vectorial(pregunta, top_k=5)
        if resultados:
            # Priorizar resultados en categorías que le interesan al usuario
            if self.contexto_temas:
                tema_favorito = self.contexto_temas.most_common(1)[0][0]
                for r in resultados:
                    if r['categoria'] == tema_favorito:
                        tipo = 'personalizada'
                        resp = f"Como te interesa {tema_favorito}, mira esto: {r['titulo']}"
                        self.actualizar_contexto(pregunta, tipo)
                        return resp, tipo, r['relevancia']

            tipo = 'directa'
            resp = f"{resultados[0]['titulo']}. {resultados[0]['snippet']}"
            self.actualizar_contexto(pregunta, tipo)
            return resp, tipo, resultados[0]['relevancia']

        tipo = 'fallback'
        resp = "No encontré algo específico. ¿Puedes darme más detalles?"
        self.actualizar_contexto(pregunta, tipo)
        return resp, tipo, 0.0

    def estadisticas_sesion(self):
        return {
            'interacciones': len(self.historial),
            'temas_interes': dict(self.contexto_temas.most_common()),
            'tipos_respuesta': Counter(h['tipo'] for h in self.historial)
        }


chatbot_ctx = ChatbotContextual(noticias, motor)

print("=== AC-6: Chatbot con Memoria de Contexto ===\n")

conversacion_sesion = [
    "¿Qué noticias hay de tecnología?",
    "Cuéntame más sobre eso",
    "¿Hay algo sobre inteligencia artificial?",
    "¿Y algo de economía?",
    "Dame otra noticia similar a la anterior",
]

for pregunta in conversacion_sesion:
    respuesta, tipo, confianza = chatbot_ctx.responder(pregunta)
    print(f"  Usuario: {pregunta}")
    print(f"  Bot [{tipo}][{confianza:.2f}]: {respuesta[:80]}...")
    print()

stats = chatbot_ctx.estadisticas_sesion()
print(f"Estadísticas de sesión:")
print(f"  Interacciones: {stats['interacciones']}")
print(f"  Temas de interés: {stats['temas_interes']}")
print(f"  Tipos de respuesta: {dict(stats['tipos_respuesta'])}")
```

### AC-7: Enriquecimiento del Knowledge Graph con Wikidata (Fase 6)

El alumno conecta entidades del Knowledge Graph local con Wikidata, enriqueciendo la información con datos externos enlazados.

```python
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF, SKOS

class EnriquecedorKG:
    """
    AC-7: Enriquece el KG local conectando con Wikidata/DBpedia.
    El alumno debe ejecutar consultas reales a endpoints SPARQL.
    """

    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.WD = Namespace("http://www.wikidata.org/entity/")
        self.WDT = Namespace("http://www.wikidata.org/prop/direct/")
        self.kg.graph.bind("wd", self.WD)
        self.kg.graph.bind("wdt", self.WDT)
        self.enlaces_externos = []

    def enlazar_entidad(self, entidad_local, wikidata_id, etiqueta):
        """Enlaza una entidad local con su equivalente en Wikidata."""
        self.kg.graph.add((entidad_local, OWL.sameAs, self.WD[wikidata_id]))
        self.kg.graph.add((entidad_local, SKOS.exactMatch, self.WD[wikidata_id]))
        self.kg.graph.add((self.WD[wikidata_id], RDFS.label, Literal(etiqueta, lang="es")))
        self.enlaces_externos.append({
            'local': str(entidad_local),
            'wikidata': wikidata_id,
            'etiqueta': etiqueta
        })

    def agregar_datos_externos(self, entidad_local, propiedades):
        """Agrega propiedades obtenidas de fuentes externas."""
        for prop, valor in propiedades.items():
            self.kg.graph.add((entidad_local, self.WDT[prop], Literal(valor)))

    def consulta_enriquecimiento(self):
        """Query SPARQL para verificar enlaces externos."""
        query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT ?local ?externo ?etiqueta
        WHERE {
            ?local owl:sameAs ?externo .
            ?externo rdfs:label ?etiqueta .
        }
        """
        return list(self.kg.graph.query(query))

    def generar_query_wikidata(self, tema):
        """Genera consultas SPARQL para Wikidata según el tema."""
        queries = {
            'tecnologia': """
# Consulta: Herramientas de NLP en Wikidata
SELECT ?item ?itemLabel ?description WHERE {
  ?item wdt:P31 wd:Q7397 .          # instancia de software
  ?item wdt:P366 wd:Q30642 .        # uso: NLP
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 10""",
            'ciencia': """
# Consulta: Investigaciones sobre cambio climático
SELECT ?item ?itemLabel ?date WHERE {
  ?item wdt:P31 wd:Q13442814 .      # instancia de artículo científico
  ?item wdt:P921 wd:Q7942 .         # tema: cambio climático
  ?item wdt:P577 ?date .
  FILTER(YEAR(?date) >= 2024)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 10""",
        }
        return queries.get(tema, "# No hay consulta predefinida para este tema")


# Enriquecer el KG del SIMANW
enriquecedor = EnriquecedorKG(kg)

# Enlazar categorías con Wikidata
DATA = Namespace("http://simanw.org/data/")
enriquecedor.enlazar_entidad(DATA["categoria_tecnologia"], "Q11016", "Tecnología de la información")
enriquecedor.enlazar_entidad(DATA["categoria_economia"], "Q159810", "Economía")
enriquecedor.enlazar_entidad(DATA["categoria_ciencia"], "Q336", "Ciencia")
enriquecedor.enlazar_entidad(DATA["categoria_gobierno"], "Q7188", "Gobierno")

# Simular datos obtenidos de Wikidata
enriquecedor.agregar_datos_externos(DATA["categoria_tecnologia"], {
    "P279": "Sector económico terciario",
    "P910": "Categoría: Tecnología de la información"
})

print("=== AC-7: Enriquecimiento con Wikidata ===\n")
print(f"Triples totales tras enriquecimiento: {kg.total_triples()}")
print(f"Enlaces externos creados: {len(enriquecedor.enlaces_externos)}")

print("\nEnlaces locales → Wikidata:")
for enlace in enriquecedor.consulta_enriquecimiento():
    local_short = str(enlace.local).split('/')[-1]
    externo_short = str(enlace.externo).split('/')[-1]
    print(f"  {local_short} → {externo_short} ({enlace.etiqueta})")

print("\nQuery sugerida para Wikidata (tecnología):")
print(enriquecedor.generar_query_wikidata('tecnologia'))
```

### AC-8: Control de calidad del corpus rastreado (Fases 1–2)

Tras incorporar al sistema las noticias obtenidas por rastreo real (no el HTML de demostración del tutorial), el alumno implementa un módulo de validación que revise el corpus antes del pipeline de lenguaje natural.

- Requisitos:
  - Generar un informe automático (texto o JSON) con: total de registros, registros inválidos o incompletos, duplicados exactos y duplicados casi idénticos (mismo título o misma URL).
  - Definir y documentar reglas mínimas de validez (campos obligatorios, longitud mínima del cuerpo, formato de fecha, coherencia de URLs).
  - Producir una lista de registros rechazados con el motivo de cada rechazo.
  - Entregar un corpus depurado utilizable en las fases siguientes.
  - Incluir un párrafo breve (máximo 200 palabras) que explique cuántos registros se descartaron y por qué.

### AC-9: Línea de tiempo y tendencias por tema (Fases 2–3)

Con las noticias ya procesadas del SIMANW (fecha y categoría o tema asignado), el alumno construye un análisis temporal que responda qué temas ganan o pierden presencia a lo largo del tiempo.

- Requisitos:
  - Agrupar noticias por periodo (semana o mes); justificar la granularidad elegida.
  - Para al menos tres temas o categorías: conteo por periodo y términos o expresiones cuya frecuencia aumente o disminuya entre el primer y el último periodo del corpus.
  - Identificar al menos un pico o una caída notable y explicarla apoyándose en títulos reales del corpus.
  - Entregar una visualización y una tabla resumen exportable.
  - Redactar una conclusión de una página con los hallazgos principales.

### AC-10: Sistema de alertas por consulta guardada (Fases 1 y 4)

El SIMANW debe permitir definir consultas permanentes (palabras clave o frases) y registrar alertas cuando entren noticias nuevas que las satisfagan.

Requisitos:
  - Persistir al menos cinco consultas guardadas con nombre y fecha de creación.
  - Al incorporar noticias nuevas al índice, determinar qué consultas se activan y con qué documentos.
  - Mantener un historial de alertas (consulta, noticia, marca de tiempo).
  - Demostrar dos ejecuciones: una sin noticias nuevas y otra tras agregar al menos cinco noticias nuevas al corpus.
  - Documentar en medio página cómo se evitan alertas duplicadas para la misma noticia y la misma consulta.

### AC-11: Estudio de usabilidad del buscador y del chatbot (Fases 4–5)

El alumno diseña y ejecuta una prueba con usuarios reales (mínimo tres personas distintas del autor) sobre el motor de búsqueda y el sistema de preguntas y respuestas del SIMANW.

- Requisitos:
  - Elaborar un guion con al menos cinco tareas (búsqueda directa, búsqueda en lenguaje natural, pregunta de conteo, pregunta de recomendación, pregunta de seguimiento que use contexto previo).
  - Aplicar un cuestionario posterior con al menos ocho ítems (facilidad, relevancia, confianza, claridad).
  - Presentar resultados anonimizados en tabla y promedios.
  - Listar al menos cinco problemas detectados y una propuesta de mejora concreta para el sistema por cada uno.
  - Incluir una reflexión breve sobre consentimiento informado y tratamiento de datos de los participantes.

### AC-12: Trazabilidad y reproducibilidad del pipeline (Fases 1–7)

El alumno demuestra que el SIMANW es reproducible: debe quedar claro qué datos entraron, qué versión del software se usó y qué artefactos se generaron.

- Requisitos:
  - Manifiesto por ejecución: fecha y hora, identificación de la versión del proyecto, fuente de noticias, número de documentos en cada etapa, referencia a los archivos de salida principales (rastreo, reporte, grafo).
  - Log estructurado de al menos una ejecución completa (rastreo → procesamiento → análisis → búsqueda → grafo → reporte).
  - Procedimiento documentado que reproduzca la ejecución a partir de datos de entrada versionados, sin depender del HTML de demostración del tutorial.
  - Checklist firmado por el alumno con pasos ejecutados y artefactos generados.
  - Anexo de una página con limitaciones conocidas (cambios en el sitio rastreado, conectividad, dependencias externas, etc.).

### AC-13: Publicación semántica y validación del grafo (Fase 6 — Web Semántica)

El alumno lleva el Knowledge Graph del SIMANW a un nivel de datos enlazados consultables y verificables según buenas prácticas de la Web Semántica.

- Requisitos:
  - Exportar el grafo en al menos dos serializaciones RDF estándar (por ejemplo Turtle y un formato alternativo acordado con el docente).
  - Publicar o entregar un volcado RDF acompañado de documentación de los prefijos, clases y propiedades de la ontología del SIMANW (glosario de términos en lenguaje natural).
  - Ejecutar al menos tres consultas SPARQL propias sobre el grafo local que no estén en el material base del curso; cada consulta debe responder una pregunta de negocio distinta (autores, sentimiento, categorías, fechas, enlaces con datasets abiertos, etc.).
  - Validar el grafo con un mecanismo formal acordado con el docente (por ejemplo reglas de forma, restricciones de ontología o validador SHACL): reportar violaciones encontradas y correcciones aplicadas.
  - Establecer al menos cinco enlaces explícitos entre recursos del grafo local y URIs externas de vocabularios o datasets públicos (Wikidata, DBpedia, Schema.org, DCAT u otro catálogo justificado); documentar el criterio de enlace.
  - Entregar un fragmento de ejemplo en JSON-LD que describa una noticia del corpus y que sea coherente con el grafo RDF exportado.
  - Redactar media página sobre cómo un agente externo podría descubrir y reutilizar estos datos sin acceso al código fuente del SIMANW.