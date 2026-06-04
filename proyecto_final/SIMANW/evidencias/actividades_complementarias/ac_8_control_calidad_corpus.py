import json
import re
from datetime import datetime
from difflib import SequenceMatcher
from urllib.parse import urlparse


class ControlCalidadCorpus:
    def __init__(self, min_cuerpo=40, umbral_similitud=0.90):
        self.min_cuerpo = min_cuerpo
        self.umbral_similitud = umbral_similitud
        self.rechazados = []
        self.duplicados_exactos = []
        self.duplicados_casi = []
        self.corpus_depurado = []

    def fecha_valida(self, fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def url_valida(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ["http", "https"] and bool(parsed.netloc)

    def titulo_similar(self, t1, t2):
        return SequenceMatcher(None, t1.lower(), t2.lower()).ratio()

    def validar_registro(self, noticia, indice):
        obligatorios = ["titulo", "cuerpo", "fecha", "url"]

        for campo in obligatorios:
            if campo not in noticia or not str(noticia[campo]).strip():
                return False, f"Campo obligatorio faltante o vacío: {campo}"

        if len(noticia["cuerpo"].strip()) < self.min_cuerpo:
            return False, "Cuerpo demasiado corto"

        if not self.fecha_valida(noticia["fecha"]):
            return False, "Formato de fecha inválido; se esperaba YYYY-MM-DD"

        if not self.url_valida(noticia["url"]):
            return False, "URL inválida o incompleta"

        return True, "válido"

    def depurar(self, noticias):
        urls_vistas = {}
        titulos_vistos = {}

        for i, noticia in enumerate(noticias):
            valido, motivo = self.validar_registro(noticia, i)

            if not valido:
                self.rechazados.append({
                    "indice": i,
                    "titulo": noticia.get("titulo", "SIN_TITULO"),
                    "motivo": motivo
                })
                continue

            titulo = noticia["titulo"].strip().lower()
            url = noticia["url"].strip().lower()

            if url in urls_vistas:
                self.duplicados_exactos.append({
                    "indice": i,
                    "motivo": "URL duplicada exacta",
                    "duplicado_de": urls_vistas[url]
                })
                continue

            duplicado_casi = False

            for titulo_previo, idx_previo in titulos_vistos.items():
                similitud = self.titulo_similar(titulo, titulo_previo)

                if similitud >= self.umbral_similitud:
                    self.duplicados_casi.append({
                        "indice": i,
                        "motivo": "Título casi idéntico",
                        "duplicado_de": idx_previo,
                        "similitud": round(similitud, 3)
                    })
                    duplicado_casi = True
                    break

            if duplicado_casi:
                continue

            urls_vistas[url] = i
            titulos_vistos[titulo] = i
            self.corpus_depurado.append(noticia)

        return self.corpus_depurado

    def generar_informe(self, total_registros):
        descartados = (
            len(self.rechazados)
            + len(self.duplicados_exactos)
            + len(self.duplicados_casi)
        )

        parrafo = (
            f"Se analizaron {total_registros} registros del corpus rastreado. "
            f"Se descartaron {descartados} registros: "
            f"{len(self.rechazados)} por campos inválidos o incompletos, "
            f"{len(self.duplicados_exactos)} por duplicados exactos de URL y "
            f"{len(self.duplicados_casi)} por títulos casi idénticos. "
            f"El corpus depurado conserva {len(self.corpus_depurado)} noticias "
            f"listas para el pipeline NLP."
        )

        return {
            "total_registros": total_registros,
            "registros_validos": len(self.corpus_depurado),
            "registros_descartados": descartados,
            "invalidos_o_incompletos": self.rechazados,
            "duplicados_exactos": self.duplicados_exactos,
            "duplicados_casi_identicos": self.duplicados_casi,
            "reglas_validez": {
                "campos_obligatorios": ["titulo", "cuerpo", "fecha", "url"],
                "longitud_minima_cuerpo": self.min_cuerpo,
                "formato_fecha": "YYYY-MM-DD",
                "url": "Debe iniciar con http o https y tener dominio",
                "duplicado_casi_identico": f"similitud de título >= {self.umbral_similitud}"
            },
            "parrafo_resumen": parrafo
        }

    def guardar_json(self, archivo, datos):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)


noticias_demo = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias y procesos.",
        "fecha": "2026-05-10",
        "url": "https://portal.com/noticias/ia-generativa"
    },
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Texto duplicado con una noticia ya registrada.",
        "fecha": "2026-05-10",
        "url": "https://portal.com/noticias/ia-generativa"
    },
    {
        "titulo": "Mercados financieros muestran volatilidad",
        "cuerpo": "Corto.",
        "fecha": "2026-05-09",
        "url": "https://portal.com/noticias/mercados"
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos abiertos y semánticos.",
        "fecha": "2026/05/06",
        "url": "https://portal.com/noticias/datos-abiertos"
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "fecha": "2026-05-06",
        "url": "https://portal.com/noticias/datos-abiertos-semantica"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio preocupante sobre el calentamiento global y sus efectos.",
        "fecha": "2026-05-08",
        "url": "https://portal.com/noticias/clima"
    }
]


print("=== AC-8: Control de Calidad del Corpus ===\n")

control = ControlCalidadCorpus(min_cuerpo=40, umbral_similitud=0.90)

corpus_depurado = control.depurar(noticias_demo)
informe = control.generar_informe(len(noticias_demo))

control.guardar_json("corpus_depurado.json", corpus_depurado)
control.guardar_json("informe_calidad_corpus.json", informe)

print(f"Total registros: {informe['total_registros']}")
print(f"Registros válidos: {informe['registros_validos']}")
print(f"Registros descartados: {informe['registros_descartados']}")

print("\nReglas mínimas de validez:")
for regla, valor in informe["reglas_validez"].items():
    print(f"- {regla}: {valor}")

print("\nRegistros rechazados:")
for r in informe["invalidos_o_incompletos"]:
    print(f"- Índice {r['indice']}: {r['motivo']}")

print("\nDuplicados exactos:")
for d in informe["duplicados_exactos"]:
    print(f"- Índice {d['indice']}: {d['motivo']}")

print("\nDuplicados casi idénticos:")
for d in informe["duplicados_casi_identicos"]:
    print(f"- Índice {d['indice']}: {d['motivo']} | Similitud: {d['similitud']}")

print("\nPárrafo resumen:")
print(informe["parrafo_resumen"])

print("\nArchivos generados:")
print("- corpus_depurado.json")
print("- informe_calidad_corpus.json")