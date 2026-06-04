from collections import Counter
from modules.search.hybrid_search import BuscadorHibrido
import unicodedata


class ChatbotSIMANW:
    def __init__(self, noticias, motor_busqueda):
        self.noticias = noticias
        self.motor = motor_busqueda
        self.historial = []
        self.contexto_temas = Counter()

        self.ultima_pregunta = None
        self.ultima_respuesta = None
        self.ultima_noticia = None
        self.ultimo_tema = None

        self.buscador_hibrido = BuscadorHibrido(self.motor, self.noticias)

    def normalizar(self, texto):
        texto = texto.lower()
        texto = ''.join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
        return texto

    def detectar_categoria(self, pregunta):
        p = self.normalizar(pregunta)

        mapa = {
            "videojuegos": ["videojuego", "videojuegos", "gaming", "gamer", "consola", "esports"],
            "salud": ["salud", "hospital", "medico", "medica", "paciente", "tratamiento", "vacuna"],
            "tecnologia": ["tecnologia", "ia", "inteligencia artificial", "software", "programacion", "python"],
            "economia": ["economia", "mercado", "mercados", "finanzas", "inversion", "exportaciones"],
            "ciencia": ["ciencia", "cientifico", "investigacion", "clima", "cambio climatico"],
            "politica": ["politica", "gobierno", "ley", "datos abiertos", "publico"]
        }

        for categoria, claves in mapa.items():
            if any(clave in p for clave in claves):
                return categoria

        return None

    def clasificar_intencion(self, pregunta):
        pregunta_lower = self.normalizar(pregunta)

        if any(w in pregunta_lower for w in ["cuantas", "total", "numero"]):
            return "conteo"

        if any(w in pregunta_lower for w in ["resumen", "resume", "sintetiza"]):
            return "resumen"

        if any(w in pregunta_lower for w in ["sentimiento", "tono", "positiv", "negativ"]):
            return "sentimiento"

        if any(w in pregunta_lower for w in ["categoria", "tema", "tipo"]):
            return "categoria"

        if any(w in pregunta_lower for w in ["recomienda", "sugiere", "similar"]):
            return "recomendacion"

        if any(w in pregunta_lower for w in ["eso", "esa", "anterior", "relacion", "relacionado", "otra", "mismo tema"]):
            return "contextual"

        return "busqueda"

    def actualizar_contexto(self, pregunta, tipo):
        self.historial.append({
            "pregunta": pregunta,
            "tipo": tipo
        })

        categoria = self.detectar_categoria(pregunta)

        if categoria:
            self.contexto_temas[categoria] += 1
            self.ultimo_tema = categoria

    def responder(self, pregunta):
        tipo = self.clasificar_intencion(pregunta)

        if tipo == "conteo":
            respuesta, confianza = self._respuesta_conteo()

        elif tipo == "resumen":
            respuesta, confianza = self._respuesta_resumen()

        elif tipo == "sentimiento":
            respuesta, confianza = self._respuesta_sentimiento()

        elif tipo == "categoria":
            respuesta, confianza = self._respuesta_categoria()

        elif tipo == "recomendacion":
            respuesta, confianza = self._respuesta_recomendacion(pregunta)

        elif tipo == "contextual":
            respuesta, confianza = self._respuesta_contextual(pregunta)

        else:
            respuesta, confianza = self._respuesta_busqueda(pregunta)

        self.actualizar_contexto(pregunta, tipo)
        self.ultima_pregunta = pregunta
        self.ultima_respuesta = respuesta

        return respuesta, tipo, confianza

    def _respuesta_conteo(self):
        cats = Counter(
            n.get("categoria_predicha", n.get("categoria_original", "general"))
            for n in self.noticias
        )

        respuesta = f"Tengo {len(self.noticias)} noticias analizadas. "
        respuesta += "Distribución por categoría: "
        respuesta += ", ".join(f"{cat}: {cant}" for cat, cant in cats.items())

        return respuesta, 1.0

    def _respuesta_resumen(self):
        respuesta = "Resumen del corpus:\n"

        for n in self.noticias[:5]:
            cat = n.get("categoria_predicha", n.get("categoria_original", "?"))
            sent = n.get("sentimiento", {}).get("etiqueta", "?")
            respuesta += f"- [{cat}][{sent}] {n['titulo']}\n"

        return respuesta, 1.0

    def _respuesta_sentimiento(self):
        sentimientos = Counter(
            n.get("sentimiento", {}).get("etiqueta", "desconocido")
            for n in self.noticias
        )

        compounds = [
            n.get("sentimiento", {}).get("compound", 0)
            for n in self.noticias
        ]

        promedio = sum(compounds) / max(len(compounds), 1)

        tono = (
            "positivo" if promedio > 0
            else "negativo" if promedio < 0
            else "neutral"
        )

        respuesta = f"Distribución de sentimiento: {dict(sentimientos)}. "
        respuesta += f"Tono general: {tono} ({promedio:+.3f})."

        return respuesta, 0.95

    def _respuesta_categoria(self):
        cats = Counter(
            n.get("categoria_predicha", n.get("categoria_original", "general"))
            for n in self.noticias
        )

        respuesta = "Categorías detectadas:\n"

        for cat, cant in cats.items():
            respuesta += f"- {cat}: {cant} noticia(s)\n"

        return respuesta, 0.95

    def buscar_por_categoria(self, categoria, pregunta="", excluir_titulo=None):
        resultados = []
        pregunta_norm = self.normalizar(pregunta)
        terminos = [t for t in pregunta_norm.split() if len(t) > 3]

        for i, n in enumerate(self.noticias):
            cat_pred = self.normalizar(n.get("categoria_predicha", ""))
            cat_orig = self.normalizar(n.get("categoria_original", ""))

            if categoria not in [cat_pred, cat_orig]:
                continue

            if excluir_titulo and n["titulo"] == excluir_titulo:
                continue

            texto = self.normalizar(f"{n['titulo']} {n['cuerpo']}")

            coincidencias = sum(1 for t in terminos if t in texto)

            relevancia = 0.60 + min(coincidencias * 0.15, 0.40)

            resultados.append({
                "doc_id": i,
                "titulo": n["titulo"],
                "snippet": n["cuerpo"][:160] + "...",
                "categoria": n.get("categoria_predicha", n.get("categoria_original", "?")),
                "sentimiento": n.get("sentimiento", {}).get("etiqueta", "?"),
                "relevancia": relevancia
            })

        resultados.sort(key=lambda r: r["relevancia"], reverse=True)

        return resultados

    def _respuesta_busqueda(self, pregunta):
        categoria = self.detectar_categoria(pregunta)

        if categoria:
            resultados = self.buscar_por_categoria(categoria, pregunta=pregunta)

            if resultados:
                mejor = resultados[0]
                self.ultima_noticia = mejor
                self.ultimo_tema = categoria

                respuesta = (
                    f"{mejor['titulo']}\n"
                    f"{mejor['snippet']}"
                )

                return respuesta, mejor.get("relevancia", 1.0)

        resultados, fuente = self.buscador_hibrido.buscar(
            consulta=pregunta,
            top_k=3,
            umbral=0.15,
            usar_rss=True,
            usar_web=False
        )

        if not resultados:
            return "No encontré información relevante para tu pregunta.", 0.0

        mejor = resultados[0]

        self.ultima_noticia = mejor
        self.ultimo_tema = mejor.get("categoria", None)

        respuesta = (
            f"{mejor['titulo']}\n"
            f"{mejor['snippet']}\n"
            f"Fuente: {fuente}"
        )

        if mejor.get("url"):
            respuesta += f"\nURL: {mejor['url']}"

        return respuesta, mejor.get("relevancia", 0.0)

    def _respuesta_recomendacion(self, pregunta):
        categoria = self.detectar_categoria(pregunta) or self.ultimo_tema

        if categoria:
            resultados = self.buscar_por_categoria(
                categoria,
                excluir_titulo=self.ultima_noticia["titulo"] if self.ultima_noticia else None
            )

            if resultados:
                self.ultima_noticia = resultados[0]
                self.ultimo_tema = categoria

                respuesta = f"Te recomiendo noticias relacionadas con {categoria}:\n"

                for r in resultados[:3]:
                    respuesta += f"- {r['titulo']}\n"

                return respuesta, 1.0

        resultados = self.motor.buscar_vectorial(pregunta, top_k=5)

        if self.ultima_noticia:
            resultados = [
                r for r in resultados
                if r["titulo"] != self.ultima_noticia["titulo"]
            ]

        if not resultados:
            return "No encontré noticias adicionales para recomendar.", 0.0

        self.ultima_noticia = resultados[0]
        self.ultimo_tema = resultados[0].get("categoria", self.ultimo_tema)

        respuesta = "Te recomiendo estas noticias:\n"

        for r in resultados[:3]:
            respuesta += f"- [{r['relevancia']:.2f}] {r['titulo']}\n"

        return respuesta, resultados[0]["relevancia"]

    def _respuesta_contextual(self, pregunta):
        if not self.ultima_pregunta and not self.ultima_noticia and not self.ultimo_tema:
            return "Todavía no tengo contexto anterior suficiente.", 0.0
    
        excluir_titulo = self.ultima_noticia["titulo"] if self.ultima_noticia else None
    
        pregunta_expandida = f"{self.ultima_pregunta or ''} {pregunta}"
    
        categoria = self.detectar_categoria(pregunta_expandida) or self.ultimo_tema
    
        candidatos = []
    
        if categoria:
            candidatos = self.buscar_por_categoria(
                categoria,
                pregunta=pregunta_expandida,
                excluir_titulo=excluir_titulo
            )
    
        if not candidatos:
            resultados, fuente = self.buscador_hibrido.buscar(
                consulta=pregunta_expandida,
                top_k=5,
                umbral=0.10,
                usar_rss=True,
                usar_web=False
            )
    
            candidatos = [
                r for r in resultados
                if not excluir_titulo or r["titulo"] != excluir_titulo
            ]
    
        if not candidatos:
            return "No encontré otra noticia distinta relacionada con la conversación anterior.", 0.0
    
        mejor = candidatos[0]
    
        self.ultima_noticia = mejor
        self.ultimo_tema = mejor.get("categoria", categoria)
    
        respuesta = (
            "Tomando como referencia la conversación anterior, encontré otra noticia relacionada:\n"
            f"{mejor['titulo']}\n"
            f"{mejor['snippet']}"
        )
    
        if mejor.get("fuente"):
            respuesta += f"\nFuente: {mejor['fuente']}"
    
        if mejor.get("url"):
            respuesta += f"\nURL: {mejor['url']}"
    
        return respuesta, mejor.get("relevancia", 1.0)

    def estadisticas_sesion(self):
        return {
            "interacciones": len(self.historial),
            "temas_interes": dict(self.contexto_temas),
            "tipos_respuesta": dict(Counter(h["tipo"] for h in self.historial))
        }