import feedparser
import json
from pathlib import Path
from datetime import datetime
from email.utils import parsedate_to_datetime
import re


class LectorRSS:
    def __init__(self, feeds):
        self.feeds = feeds
        self.resultados = []

    def limpiar_html(self, texto):
        texto = re.sub(r"<[^>]+>", " ", texto or "")
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto

    def normalizar_fecha(self, fecha):
        if not fecha:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            return parsedate_to_datetime(fecha).strftime("%Y-%m-%d")
        except Exception:
            try:
                return datetime.fromisoformat(fecha[:10]).strftime("%Y-%m-%d")
            except Exception:
                return datetime.now().strftime("%Y-%m-%d")

    def leer(self):
        self.resultados = []

        for fuente in self.feeds:
            feed = feedparser.parse(fuente["url"])

            for entrada in feed.entries:
                titulo = entrada.get("title", "").strip()

                cuerpo = (
                    entrada.get("summary", "")
                    or entrada.get("description", "")
                    or entrada.get("title", "")
                )

                cuerpo = self.limpiar_html(cuerpo)

                fecha = (
                    entrada.get("published", "")
                    or entrada.get("updated", "")
                    or ""
                )

                noticia = {
                    "titulo": titulo,
                    "cuerpo": cuerpo,
                    "fecha": self.normalizar_fecha(fecha),
                    "autor": fuente.get("nombre", "Fuente RSS"),
                    "categoria_original": self.inferir_categoria(titulo, cuerpo, fuente.get("categoria", "general")),
                    "url": entrada.get("link", "").strip(),
                    "fuente": "rss"
                }

                self.resultados.append(noticia)

        return self.resultados

    def inferir_categoria(self, titulo, cuerpo, categoria_default="general"):
        texto = f"{titulo} {cuerpo}".lower()
    
        reglas = {
            "tecnologia": [
                "inteligencia artificial", "software", "tecnología",
                "ciberseguridad", "datos", "digital", "programación"
            ],
            "salud": [
                "salud", "hospital", "médico", "paciente",
                "vacuna", "enfermedad", "tratamiento"
            ],
            "economia": [
                "economía", "mercado", "finanzas", "inflación",
                "inversión", "banco", "dólar", "empleo"
            ],
            "ciencia": [
                "ciencia", "investigación", "científico",
                "clima", "descubrimiento", "espacio", "laboratorio"
            ],
            "politica": [
                "gobierno", "presidente", "ley", "congreso",
                "elecciones", "política", "ministro"
            ],
            "videojuegos": [
                "videojuego", "videojuegos", "gaming",
                "consola", "nintendo", "xbox", "playstation", "esports"
            ],
            "deportes": [
                "champions", "league", "fútbol", "liga",
                "partido", "gol", "mundial", "uefa"
            ]
        }
    
        puntajes = {}
    
        for categoria, palabras in reglas.items():
            puntajes[categoria] = sum(1 for p in palabras if p in texto)
    
        mejor_categoria = max(puntajes, key=puntajes.get)
    
        if puntajes[mejor_categoria] == 0:
            return categoria_default
    
        return mejor_categoria

    def guardar_json(self, ruta="data/raw/noticias_rss.json"):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)