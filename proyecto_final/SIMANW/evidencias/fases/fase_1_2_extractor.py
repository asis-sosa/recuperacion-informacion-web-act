from bs4 import BeautifulSoup

html_portal_noticias = """
<!DOCTYPE html>
<html>
<body>
  <main id="contenido">
    <article class="noticia" data-categoria="tecnologia">
      <h2>Avances en IA Generativa revolucionan la industria</h2>
      <p class="cuerpo">Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.</p>
      <div class="meta">
        <span class="fecha">2026-05-10</span>
        <span class="autor">María García</span>
        <a href="/noticias/ia-generativa-2026" class="leer-mas">Leer más</a>
      </div>
    </article>

    <article class="noticia" data-categoria="economia">
      <h2>Mercados financieros muestran volatilidad ante incertidumbre global</h2>
      <p class="cuerpo">Los principales índices bursátiles registraron caídas significativas.</p>
      <div class="meta">
        <span class="fecha">2026-05-09</span>
        <span class="autor">Carlos Ruiz</span>
        <a href="/noticias/mercados-volatilidad" class="leer-mas">Leer más</a>
      </div>
    </article>

    <article class="noticia" data-categoria="ciencia">
      <h2>Descubrimiento científico sobre cambio climático alarma a expertos</h2>
      <p class="cuerpo">Un equipo internacional publicó un estudio sobre el calentamiento global.</p>
      <div class="meta">
        <span class="fecha">2026-05-08</span>
        <span class="autor">Ana López</span>
        <a href="/noticias/clima-estudio-2026" class="leer-mas">Leer más</a>
      </div>
    </article>
  </main>
</body>
</html>
"""


class ExtractorNoticias:
    def __init__(self):
        self.noticias_extraidas = []
        self.errores = []

    def extraer_de_html(self, html_content, url_base="https://portal.com"):
        soup = BeautifulSoup(html_content, "html.parser")
        articulos = soup.find_all("article", class_="noticia")

        for art in articulos:
            try:
                noticia = {
                    "titulo": art.find("h2").get_text(strip=True),
                    "cuerpo": art.find("p", class_="cuerpo").get_text(strip=True),
                    "fecha": art.find("span", class_="fecha").get_text(strip=True),
                    "autor": art.find("span", class_="autor").get_text(strip=True),
                    "categoria_original": art.get("data-categoria", "sin_categoria"),
                    "url": url_base + art.find("a", class_="leer-mas")["href"],
                    "fuente": url_base,
                }

                self.noticias_extraidas.append(noticia)

            except Exception as e:
                self.errores.append(str(e))

        return self.noticias_extraidas

    def resumen_extraccion(self):
        return {
            "total_extraidas": len(self.noticias_extraidas),
            "errores": len(self.errores),
            "categorias": list(set(n["categoria_original"] for n in self.noticias_extraidas)),
            "rango_fechas": (
                min(n["fecha"] for n in self.noticias_extraidas),
                max(n["fecha"] for n in self.noticias_extraidas),
            ) if self.noticias_extraidas else None,
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
    print(f"{i}. [{n['fecha']}] [{n['categoria_original']}] {n['titulo']}")
    print(f"   Autor: {n['autor']}")
    print(f"   URL: {n['url']}")