import feedparser
import json
from pathlib import Path


class LectorRSS:
    def __init__(self, feeds):
        self.feeds = feeds
        self.resultados = []

    def leer(self):
        for fuente in self.feeds:
            feed = feedparser.parse(fuente["url"])

            for entrada in feed.entries:
                noticia = {
                    "titulo": entrada.get("title", ""),
                    "cuerpo": entrada.get("summary", ""),
                    "fecha": entrada.get("published", ""),
                    "autor": fuente.get("nombre", "Fuente RSS"),
                    "categoria_original": fuente.get("categoria", "general"),
                    "url": entrada.get("link", "")
                }

                self.resultados.append(noticia)

        return self.resultados

    def guardar_json(self, ruta="data/raw/noticias_raw.json"):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)