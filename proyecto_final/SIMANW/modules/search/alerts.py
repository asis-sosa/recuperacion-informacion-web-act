import json
from datetime import datetime
from pathlib import Path


class SistemaAlertas:
    def __init__(self):
        self.consultas_guardadas = []
        self.historial_alertas = []
        self.alertas_emitidas = set()

    def cargar_consultas_base(self):
        self.consultas_guardadas = [
            {
                "id": 1,
                "nombre": "Alerta IA",
                "consulta": "inteligencia artificial",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 2,
                "nombre": "Alerta Python",
                "consulta": "python",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 3,
                "nombre": "Alerta Economía",
                "consulta": "mercados financieros",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 4,
                "nombre": "Alerta Gobierno",
                "consulta": "datos abiertos",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 5,
                "nombre": "Alerta Clima",
                "consulta": "cambio climático",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def coincide(self, consulta, noticia):
        texto = f"{noticia['titulo']} {noticia['cuerpo']}".lower()
        terminos = consulta.lower().split()

        return all(t in texto for t in terminos)

    def revisar(self, noticias):
        alertas_nuevas = []

        if not self.consultas_guardadas:
            self.cargar_consultas_base()

        for consulta in self.consultas_guardadas:
            for idx, noticia in enumerate(noticias):
                noticia_id = noticia.get("id", idx + 1)
                clave = (consulta["id"], noticia_id)

                if clave in self.alertas_emitidas:
                    continue

                if self.coincide(consulta["consulta"], noticia):
                    alerta = {
                        "consulta_id": consulta["id"],
                        "consulta_nombre": consulta["nombre"],
                        "consulta": consulta["consulta"],
                        "noticia_id": noticia_id,
                        "titulo": noticia["titulo"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    self.historial_alertas.append(alerta)
                    self.alertas_emitidas.add(clave)
                    alertas_nuevas.append(alerta)

        return alertas_nuevas

    def guardar(self, ruta="outputs/alerts/historial_alertas.json"):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.historial_alertas, f, ensure_ascii=False, indent=2)

        return ruta