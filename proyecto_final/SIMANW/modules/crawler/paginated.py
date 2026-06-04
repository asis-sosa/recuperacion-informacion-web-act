import time
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser


class RastreadorPaginado:
    def __init__(
        self,
        url_base,
        selector_articulos,
        selector_siguiente,
        delay=3,
        max_paginas=5,
        modo_demo=True
    ):
        self.url_base = url_base
        self.selector_articulos = selector_articulos
        self.selector_siguiente = selector_siguiente
        self.delay = delay
        self.max_paginas = max_paginas
        self.modo_demo = modo_demo
        self.resultados = []

    def robots_permite(self, url):
        if self.modo_demo:
            return True

        robots_url = urljoin(url, "/robots.txt")

        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()

        return rp.can_fetch("*", url)

    def obtener_html(self, url_actual, pagina):
        if self.modo_demo:
            return f"""
            <div class="articulos">
              <article>
                <h2>Noticia {pagina*5 - 4} de ejemplo paginado</h2>
                <p>Contenido de la noticia extraída del sitio simulado.</p>
                <a href="/noticia/{pagina*5 - 4}">Leer</a>
              </article>
              <article>
                <h2>Noticia {pagina*5 - 3} de ejemplo paginado</h2>
                <p>Otra noticia con información relevante.</p>
                <a href="/noticia/{pagina*5 - 3}">Leer</a>
              </article>
              <article>
                <h2>Noticia {pagina*5 - 2} de ejemplo paginado</h2>
                <p>Tercera noticia de esta página.</p>
                <a href="/noticia/{pagina*5 - 2}">Leer</a>
              </article>
              <article>
                <h2>Noticia {pagina*5 - 1} de ejemplo paginado</h2>
                <p>Cuarta noticia del bloque de rastreo.</p>
                <a href="/noticia/{pagina*5 - 1}">Leer</a>
              </article>
              <article>
                <h2>Noticia {pagina*5} de ejemplo paginado</h2>
                <p>Quinta noticia encontrada por el rastreador.</p>
                <a href="/noticia/{pagina*5}">Leer</a>
              </article>
            </div>
            <a class="next-page" href="/noticias?page={pagina + 1}">Siguiente</a>
            """

        response = requests.get(url_actual, timeout=10)
        response.raise_for_status()
        return response.text

    def extraer_pagina(self, html, url_actual):
        soup = BeautifulSoup(html, "html.parser")
        articulos = soup.select(self.selector_articulos)

        noticias = []

        for art in articulos:
            titulo_elem = art.find(["h1", "h2", "h3"])
            parrafo_elem = art.find("p")
            enlace_elem = art.find("a")

            if titulo_elem:
                noticias.append({
                    "titulo": titulo_elem.get_text(strip=True),
                    "resumen": parrafo_elem.get_text(strip=True) if parrafo_elem else "",
                    "url": urljoin(url_actual, enlace_elem["href"]) if enlace_elem and enlace_elem.get("href") else url_actual
                })

        return noticias

    def obtener_siguiente_pagina(self, html, url_actual):
        soup = BeautifulSoup(html, "html.parser")
        siguiente = soup.select_one(self.selector_siguiente)

        if siguiente and siguiente.get("href"):
            return urljoin(url_actual, siguiente["href"])

        return None

    def rastrear(self):
        url_actual = self.url_base
        pagina = 1

        while url_actual and pagina <= self.max_paginas:
            if not self.robots_permite(url_actual):
                break

            html = self.obtener_html(url_actual, pagina)
            noticias = self.extraer_pagina(html, url_actual)
            self.resultados.extend(noticias)

            siguiente = self.obtener_siguiente_pagina(html, url_actual)

            if not siguiente:
                break

            url_actual = siguiente
            pagina += 1

            if not self.modo_demo:
                time.sleep(self.delay)

        return self.resultados

    def guardar_json(self, archivo):
        ruta = Path(archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)

        return len(self.resultados)