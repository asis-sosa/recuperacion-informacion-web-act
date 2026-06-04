from bs4 import BeautifulSoup

html_portal_noticias = """
<!DOCTYPE html>
<html>
<head><title>Portal de Noticias - SIMANW</title></head>
<body>
  <nav>
    <a href="/">Inicio</a>
    <a href="/tech">Tech</a>
    <a href="/ciencia">Ciencia</a>
  </nav>

  <main id="contenido">
    <h1>Últimas Noticias</h1>

    <article class="noticia" data-categoria="tecnologia">
      <h2>Avances en IA Generativa revolucionan la industria</h2>
      <p class="cuerpo">Los nuevos modelos de inteligencia artificial generativa
      están transformando múltiples industrias.</p>
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

soup = BeautifulSoup(html_portal_noticias, "html.parser")

print("=== FASE 1.1: Parsing del DOM ===\n")

print(f"Título del portal: {soup.title.string}")

navegacion = [a.get_text(strip=True) for a in soup.nav.find_all("a")]
print(f"Secciones de navegación: {navegacion}")

articulos = soup.find_all("article", class_="noticia")
print(f"Total de artículos: {len(articulos)}")

tendencias = [li.a.get_text(strip=True) for li in soup.aside.find_all("li")]
print(f"Tendencias: {tendencias}")

print("\nEstructura del DOM detectada:")
print("  <html>")
print("    <head> → título")
print("    <body>")
print(f"      <nav> → {len(navegacion)} enlaces")
print(f"      <main> → {len(articulos)} artículos")
print("      <aside> → tendencias")
print("      <footer> → copyright")

print("\nArtículos detectados:")
for articulo in articulos:
    titulo = articulo.find("h2").get_text(strip=True)
    categoria = articulo.get("data-categoria")
    fecha = articulo.find("span", class_="fecha").get_text(strip=True)
    autor = articulo.find("span", class_="autor").get_text(strip=True)

    print(f"- [{fecha}] [{categoria}] {titulo} | Autor: {autor}")