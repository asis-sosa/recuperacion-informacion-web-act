import json
from pathlib import Path


class GestorCorpus:
    def __init__(self, ruta_base="data/raw/noticias_base.json"):
        self.ruta_base = Path(ruta_base)
        self.ruta_base.parent.mkdir(parents=True, exist_ok=True)

    def cargar(self):
        if not self.ruta_base.exists():
            return []

        with open(self.ruta_base, "r", encoding="utf-8") as f:
            return json.load(f)

    def guardar(self, noticias):
        with open(self.ruta_base, "w", encoding="utf-8") as f:
            json.dump(noticias, f, ensure_ascii=False, indent=2)

    def normalizar_noticia_externa(self, noticia, categoria_default="general"):
        return {
            "titulo": noticia.get("titulo", "").strip(),
            "cuerpo": noticia.get("snippet", noticia.get("cuerpo", "")).strip(),
            "fecha": noticia.get("fecha", "2026-06-04"),
            "autor": noticia.get("fuente", "Fuente externa"),
            "categoria_original": noticia.get("categoria", categoria_default),
            "url": noticia.get("url", "")
        }

    def agregar_noticias(self, nuevas):
        actuales = self.cargar()

        urls_existentes = {
            n.get("url", "").strip().lower()
            for n in actuales
            if n.get("url")
        }

        titulos_existentes = {
            n.get("titulo", "").strip().lower()
            for n in actuales
        }

        agregadas = []
        duplicadas = []

        for n in nuevas:
            noticia = self.normalizar_noticia_externa(n)

            url = noticia["url"].lower()
            titulo = noticia["titulo"].lower()

            if not noticia["titulo"] or not noticia["cuerpo"]:
                continue

            if url in urls_existentes or titulo in titulos_existentes:
                duplicadas.append(noticia)
                continue

            actuales.append(noticia)
            agregadas.append(noticia)

            if url:
                urls_existentes.add(url)

            titulos_existentes.add(titulo)

        self.guardar(actuales)

        return {
            "agregadas": agregadas,
            "duplicadas": duplicadas,
            "total_corpus": len(actuales)
        }