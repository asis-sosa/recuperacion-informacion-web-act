import json
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
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
            }
        }


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_json(ruta, datos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)