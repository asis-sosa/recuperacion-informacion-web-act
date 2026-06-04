import json
from datetime import datetime


class SistemaAlertas:
    def __init__(self):
        self.consultas_guardadas = []
        self.corpus = []
        self.historial_alertas = []
        self.alertas_emitidas = set()

    def agregar_consulta(self, nombre, consulta):
        self.consultas_guardadas.append({
            "id": len(self.consultas_guardadas) + 1,
            "nombre": nombre,
            "consulta": consulta.lower(),
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def agregar_noticias(self, noticias_nuevas):
        inicio = len(self.corpus)

        for i, noticia in enumerate(noticias_nuevas):
            noticia["id"] = inicio + i + 1
            self.corpus.append(noticia)

        return noticias_nuevas

    def coincide(self, consulta, noticia):
        texto = f"{noticia['titulo']} {noticia['cuerpo']}".lower()
        terminos = consulta.split()

        return all(t in texto for t in terminos)

    def revisar_noticias_nuevas(self, noticias_nuevas):
        alertas_nuevas = []

        for consulta in self.consultas_guardadas:
            for noticia in noticias_nuevas:
                clave_alerta = (consulta["id"], noticia["id"])

                if clave_alerta in self.alertas_emitidas:
                    continue

                if self.coincide(consulta["consulta"], noticia):
                    alerta = {
                        "consulta_id": consulta["id"],
                        "consulta_nombre": consulta["nombre"],
                        "consulta": consulta["consulta"],
                        "noticia_id": noticia["id"],
                        "titulo": noticia["titulo"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    self.historial_alertas.append(alerta)
                    self.alertas_emitidas.add(clave_alerta)
                    alertas_nuevas.append(alerta)

        return alertas_nuevas

    def guardar_estado(self):
        with open("consultas_guardadas.json", "w", encoding="utf-8") as f:
            json.dump(self.consultas_guardadas, f, ensure_ascii=False, indent=2)

        with open("historial_alertas.json", "w", encoding="utf-8") as f:
            json.dump(self.historial_alertas, f, ensure_ascii=False, indent=2)

    def documentacion_duplicados(self):
        return (
            "Para evitar alertas duplicadas, el sistema conserva un conjunto llamado "
            "alertas_emitidas. En este conjunto se almacena una clave única formada por "
            "el identificador de la consulta guardada y el identificador de la noticia. "
            "Antes de registrar una nueva alerta, el sistema verifica si esa combinación "
            "consulta-noticia ya existe. Si existe, la alerta se ignora; si no existe y la "
            "noticia satisface la consulta, se registra en el historial y la clave se agrega "
            "al conjunto. Con esta regla, una misma noticia puede activar consultas distintas, "
            "pero no puede activar repetidamente la misma consulta. Esto permite ejecutar el "
            "módulo varias veces sin inflar artificialmente el historial de alertas."
        )


sistema = SistemaAlertas()

consultas = [
    ("Alerta IA", "inteligencia artificial"),
    ("Alerta Python", "python"),
    ("Alerta Economía", "mercados financieros"),
    ("Alerta Gobierno", "datos abiertos"),
    ("Alerta Clima", "cambio climático")
]

for nombre, consulta in consultas:
    sistema.agregar_consulta(nombre, consulta)


print("=== AC-10: Sistema de Alertas por Consulta Guardada ===\n")

print("Consultas guardadas:")
for c in sistema.consultas_guardadas:
    print(f"- [{c['id']}] {c['nombre']}: {c['consulta']} | Creada: {c['fecha_creacion']}")


print("\n--- Ejecución 1: Sin noticias nuevas ---")
noticias_nuevas_1 = []
alertas_1 = sistema.revisar_noticias_nuevas(noticias_nuevas_1)

if not alertas_1:
    print("No se generaron alertas porque no ingresaron noticias nuevas.")


print("\n--- Ejecución 2: Con cinco noticias nuevas ---")

noticias_nuevas_2 = [
    {
        "titulo": "Avances en inteligencia artificial generativa impactan la educación",
        "cuerpo": "Nuevos modelos de inteligencia artificial se aplican en universidades y plataformas digitales."
    },
    {
        "titulo": "Python se mantiene como lenguaje clave para ciencia de datos",
        "cuerpo": "La comunidad de programación destaca el uso de Python en automatización y análisis."
    },
    {
        "titulo": "Mercados financieros reaccionan ante nuevas tasas de interés",
        "cuerpo": "Los mercados financieros muestran volatilidad por decisiones del banco central."
    },
    {
        "titulo": "Gobierno publica portal de datos abiertos",
        "cuerpo": "La nueva plataforma de datos abiertos busca mejorar la transparencia pública."
    },
    {
        "titulo": "Estudio alerta sobre cambio climático y emisiones",
        "cuerpo": "Investigadores advierten que el cambio climático continúa afectando ecosistemas."
    }
]

noticias_agregadas = sistema.agregar_noticias(noticias_nuevas_2)
alertas_2 = sistema.revisar_noticias_nuevas(noticias_agregadas)

print(f"Noticias nuevas incorporadas: {len(noticias_agregadas)}")
print(f"Alertas generadas: {len(alertas_2)}")

for alerta in alertas_2:
    print(
        f"- Consulta '{alerta['consulta_nombre']}' activada por noticia "
        f"{alerta['noticia_id']}: {alerta['titulo']}"
    )


print("\n--- Revisión adicional para comprobar duplicados ---")
alertas_repetidas = sistema.revisar_noticias_nuevas(noticias_agregadas)

if not alertas_repetidas:
    print("No se generaron alertas repetidas para las mismas noticias y consultas.")


sistema.guardar_estado()

print("\nArchivos generados:")
print("- consultas_guardadas.json")
print("- historial_alertas.json")

print("\nDocumentación sobre control de duplicados:")
print(sistema.documentacion_duplicados())