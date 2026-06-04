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

archivo_salida = "noticias_paginadas.json"
total = rastreador_paginado.guardar_json(archivo_salida)

print(f"\nArchivo generado: {archivo_salida}")
print(f"Noticias guardadas: {total}")