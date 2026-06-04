import feedparser
from duckduckgo_search import DDGS


class BuscadorHibrido:
    def __init__(self, motor_local, noticias_locales):
        self.motor_local = motor_local
        self.noticias_locales = noticias_locales

        self.feeds = [
            {
                "nombre": "BBC Mundo",
                "url": "https://feeds.bbci.co.uk/mundo/rss.xml",
                "categoria": "general"
            },
            {
                "nombre": "El País Tecnología",
                "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada",
                "categoria": "tecnologia"
            }
        ]

    def buscar_local(self, consulta, top_k=5, umbral=0.10):
        resultados = self.motor_local.buscar_vectorial(
            consulta,
            top_k=len(self.noticias_locales)
        )

        resultados = [
            r for r in resultados
            if r["relevancia"] >= umbral
        ]

        return resultados[:top_k]

    def buscar_rss(self, consulta, top_k=5):
        consulta_lower = consulta.lower()
        resultados = []

        for fuente in self.feeds:
            try:
                feed = feedparser.parse(fuente["url"])

                for entrada in feed.entries:
                    titulo = entrada.get("title", "")
                    resumen = entrada.get("summary", "")
                    url = entrada.get("link", "")

                    texto = f"{titulo} {resumen}".lower()

                    if any(palabra in texto for palabra in consulta_lower.split()):
                        resultados.append({
                            "titulo": titulo,
                            "snippet": resumen[:180] + "...",
                            "categoria": fuente["categoria"],
                            "sentimiento": "?",
                            "relevancia": 0.60,
                            "url": url,
                            "fuente": f"RSS - {fuente['nombre']}"
                        })

            except Exception:
                continue

        return resultados[:top_k]

    def buscar_web(self, consulta, top_k=5):
        resultados = []

        try:
            with DDGS() as ddgs:
                busqueda = ddgs.text(
                    consulta,
                    max_results=top_k
                )

                for r in busqueda:
                    resultados.append({
                        "titulo": r.get("title", ""),
                        "snippet": r.get("body", ""),
                        "categoria": "web",
                        "sentimiento": "?",
                        "relevancia": 0.40,
                        "url": r.get("href", ""),
                        "fuente": "Web externa"
                    })

        except Exception as e:
            resultados.append({
                "titulo": "No fue posible consultar la web externa",
                "snippet": str(e),
                "categoria": "error",
                "sentimiento": "?",
                "relevancia": 0.0,
                "url": "",
                "fuente": "Error"
            })

        return resultados

    def buscar(self, consulta, top_k=5, umbral=0.10, usar_rss=True, usar_web=True):
        resultados_locales = self.buscar_local(consulta, top_k, umbral)

        if resultados_locales:
            return resultados_locales, "Corpus local"

        if usar_rss:
            resultados_rss = self.buscar_rss(consulta, top_k)

            if resultados_rss:
                return resultados_rss, "Feeds RSS"

        if usar_web:
            resultados_web = self.buscar_web(consulta, top_k)

            if resultados_web:
                return resultados_web, "Web externa"

        return [], "Sin resultados"