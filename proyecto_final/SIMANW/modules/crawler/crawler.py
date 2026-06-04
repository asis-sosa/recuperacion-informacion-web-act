import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class RastreadorNoticias:
    def __init__(
        self,
        url_base="https://ejemplo-noticias.com/ultimas",
        selector_articulos="article",
        selector_siguiente="a.next-page",
        delay=3,
        max_paginas=4,
        modo_demo=True
    ):
        self.url_base = url_base
        self.selector_articulos = selector_articulos
        self.selector_siguiente = selector_siguiente
        self.delay = delay
        self.max_paginas = max_paginas
        self.modo_demo = modo_demo
        self.resultados = []

    def obtener_html(self, url_actual, pagina):
        if self.modo_demo:
            return f"""
            <html>
            <body>
              <main>
                <article data-categoria="tecnologia">
                  <h2>Avances en IA Generativa página {pagina}</h2>
                  <p>La inteligencia artificial generativa transforma industrias, software y automatización.</p>
                  <span class="fecha">2026-05-{pagina:02d}</span>
                  <span class="autor">Autor Tecnología</span>
                  <a href="/noticias/ia-{pagina}">Leer más</a>
                </article>

                <article data-categoria="economia">
                  <h2>Mercados financieros muestran volatilidad página {pagina}</h2>
                  <p>Los mercados financieros registran cambios por inflación, tasas de interés e inversión.</p>
                  <span class="fecha">2026-05-{pagina + 1:02d}</span>
                  <span class="autor">Autor Economía</span>
                  <a href="/noticias/economia-{pagina}">Leer más</a>
                </article>

                <article data-categoria="ciencia">
                  <h2>Cambio climático preocupa a científicos página {pagina}</h2>
                  <p>Investigadores reportan nuevas evidencias sobre calentamiento global y emisiones.</p>
                  <span class="fecha">2026-05-{pagina + 2:02d}</span>
                  <span class="autor">Autor Ciencia</span>
                  <a href="/noticias/ciencia-{pagina}">Leer más</a>
                </article>
              </main>
              <a class="next-page" href="/noticias?page={pagina + 1}">Siguiente</a>
            </body>
            </html>
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
            cuerpo_elem = art.find("p")
            enlace_elem = art.find("a")
            fecha_elem = art.find("span", class_="fecha")
            autor_elem = art.find("span", class_="autor")

            if not titulo_elem:
                continue

            noticia = {
                "titulo": titulo_elem.get_text(strip=True),
                "cuerpo": cuerpo_elem.get_text(strip=True) if cuerpo_elem else "",
                "fecha": fecha_elem.get_text(strip=True) if fecha_elem else datetime.now().strftime("%Y-%m-%d"),
                "autor": autor_elem.get_text(strip=True) if autor_elem else "Desconocido",
                "categoria_original": art.get("data-categoria", "general"),
                "url": urljoin(url_actual, enlace_elem["href"]) if enlace_elem and enlace_elem.get("href") else url_actual,
                "fuente": url_actual,
                "fecha_rastreo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            noticias.append(noticia)

        return noticias

    def obtener_siguiente_pagina(self, html, url_actual):
        soup = BeautifulSoup(html, "html.parser")
        siguiente = soup.select_one(self.selector_siguiente)

        if siguiente and siguiente.get("href"):
            return urljoin(url_actual, siguiente["href"])

        return None

    def rastrear(self):
        with open(
            "data/raw/noticias_base.json",
            "r",
            encoding="utf-8"
        ) as f:
            self.resultados = json.load(f)
    
        return self.resultados

    def guardar_json(self, ruta_salida="data/raw/noticias_raw.json"):
        ruta = Path(ruta_salida)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)

        return ruta