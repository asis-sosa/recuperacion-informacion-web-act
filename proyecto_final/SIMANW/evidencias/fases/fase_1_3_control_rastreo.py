from urllib.parse import urlparse, urljoin
from collections import deque


class ControlRastreo:
    def __init__(self, url_semilla, modo="dominio", max_paginas=50, delay=2):
        self.url_semilla = url_semilla
        self.dominio = urlparse(url_semilla).netloc
        self.modo = modo
        self.max_paginas = max_paginas
        self.delay = delay
        self.visitadas = set()
        self.cola = deque([url_semilla])
        self.rechazadas = []

    def url_permitida(self, url):
        parsed = urlparse(url)

        if self.modo == "dominio":
            return parsed.netloc == self.dominio

        elif self.modo == "directorio":
            base_path = urlparse(self.url_semilla).path.rsplit("/", 1)[0]
            return parsed.netloc == self.dominio and parsed.path.startswith(base_path)

        elif self.modo == "subdominio":
            return parsed.netloc.endswith(self.dominio.split(".", 1)[-1])

        return False

    def registrar_visita(self, url):
        self.visitadas.add(url)

    def agregar_enlaces(self, enlaces):
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
        if self.cola and len(self.visitadas) < self.max_paginas:
            url = self.cola.popleft()
            self.registrar_visita(url)
            return url

        return None

    def estado(self):
        return {
            "visitadas": len(self.visitadas),
            "en_cola": len(self.cola),
            "rechazadas": len(self.rechazadas),
            "limite": self.max_paginas,
            "completado": len(self.visitadas) >= self.max_paginas or not self.cola,
        }


control = ControlRastreo(
    "https://portal-noticias.com/noticias/",
    modo="directorio",
    max_paginas=10,
    delay=2,
)

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
print(f"Dominio permitido: {control.dominio}")
print(f"Modo: {control.modo}")
print(f"Máximo de páginas: {control.max_paginas}")
print(f"Delay entre peticiones: {control.delay}s")

agregados = control.agregar_enlaces(enlaces_descubiertos)

print(f"\nEnlaces descubiertos: {len(enlaces_descubiertos)}")
print(f"Agregados a la cola: {agregados}")
print(f"Rechazados: {len(control.rechazadas)}")

print("\nURLs rechazadas:")
for url in control.rechazadas:
    print(f"- {url}")

print("\nSimulación de rastreo:")
while True:
    url = control.siguiente()

    if not url:
        break

    print(f"Visitando: {url}")

print(f"\nEstado final: {control.estado()}")