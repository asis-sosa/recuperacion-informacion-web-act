import re
import csv
from collections import Counter, defaultdict
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "La inteligencia artificial generativa transforma empresas, software y automatización.",
        "fecha": "2026-01-10",
        "categoria_predicha": "tecnologia"
    },
    {
        "titulo": "Python gana popularidad en desarrollo de inteligencia artificial",
        "cuerpo": "Python, machine learning y programación dominan los proyectos tecnológicos.",
        "fecha": "2026-01-25",
        "categoria_predicha": "tecnologia"
    },
    {
        "titulo": "Mercados financieros inician el año con volatilidad",
        "cuerpo": "La inflación y las tasas de interés preocupan a inversionistas.",
        "fecha": "2026-01-16",
        "categoria_predicha": "economia"
    },
    {
        "titulo": "Científicos alertan sobre emisiones contaminantes",
        "cuerpo": "El cambio climático y las emisiones de carbono muestran señales preocupantes.",
        "fecha": "2026-02-03",
        "categoria_predicha": "ciencia"
    },
    {
        "titulo": "Gobierno presenta estrategia nacional de datos abiertos",
        "cuerpo": "El gobierno impulsa transparencia, datos abiertos y tecnología semántica.",
        "fecha": "2026-02-17",
        "categoria_predicha": "politica"
    },
    {
        "titulo": "Empresas aceleran adopción de IA en sus procesos",
        "cuerpo": "La automatización, los modelos generativos y el software empresarial aumentan.",
        "fecha": "2026-03-05",
        "categoria_predicha": "tecnologia"
    },
    {
        "titulo": "Inflación mensual muestra ligera reducción",
        "cuerpo": "Los mercados reaccionan positivamente ante menor inflación y estabilidad financiera.",
        "fecha": "2026-03-14",
        "categoria_predicha": "economia"
    },
    {
        "titulo": "Nuevo estudio confirma aumento del calentamiento global",
        "cuerpo": "Investigadores publican datos sobre clima, temperatura y cambio climático.",
        "fecha": "2026-03-22",
        "categoria_predicha": "ciencia"
    },
    {
        "titulo": "Datos abiertos permiten monitorear gasto público",
        "cuerpo": "La transparencia gubernamental mejora con datasets públicos y portales abiertos.",
        "fecha": "2026-04-09",
        "categoria_predicha": "politica"
    },
    {
        "titulo": "IA generativa domina la agenda tecnológica del mes",
        "cuerpo": "La inteligencia artificial, los modelos generativos y la programación siguen creciendo.",
        "fecha": "2026-04-20",
        "categoria_predicha": "tecnologia"
    },
    {
        "titulo": "Bolsa cae por incertidumbre económica internacional",
        "cuerpo": "Los mercados financieros registran pérdidas por inflación y riesgo global.",
        "fecha": "2026-05-04",
        "categoria_predicha": "economia"
    },
    {
        "titulo": "Investigadores proponen soluciones contra cambio climático",
        "cuerpo": "La ciencia climática propone reducir emisiones y mejorar políticas ambientales.",
        "fecha": "2026-05-13",
        "categoria_predicha": "ciencia"
    }
]


STOPWORDS = {
    "sobre", "para", "con", "los", "las", "una", "uno", "del", "por",
    "que", "sus", "más", "este", "esta", "entre", "ante", "muestra",
    "muestran", "noticia", "nuevo", "nueva"
}


class AnalizadorTendencias:
    def __init__(self, noticias):
        self.noticias = noticias
        self.df = pd.DataFrame(noticias)
        self.df["fecha"] = pd.to_datetime(self.df["fecha"])
        self.df["periodo"] = self.df["fecha"].dt.to_period("M").astype(str)

    def justificar_granularidad(self):
        return (
            "Se utiliza granularidad mensual porque el corpus de demostración contiene "
            "noticias distribuidas en varios meses. Esta escala permite observar cambios "
            "de presencia temática sin generar demasiados periodos vacíos."
        )

    def tabla_conteo_por_periodo(self):
        tabla = pd.crosstab(
            self.df["periodo"],
            self.df["categoria_predicha"]
        )
        return tabla

    def limpiar_tokens(self, texto):
        texto = texto.lower()
        texto = re.sub(r"[^\w\sáéíóúñü]", " ", texto)
        tokens = [
            t for t in texto.split()
            if len(t) > 3 and t not in STOPWORDS
        ]
        return tokens

    def terminos_por_categoria_y_periodo(self):
        resultado = defaultdict(lambda: defaultdict(Counter))

        for _, row in self.df.iterrows():
            categoria = row["categoria_predicha"]
            periodo = row["periodo"]
            texto = f"{row['titulo']} {row['cuerpo']}"
            tokens = self.limpiar_tokens(texto)

            resultado[categoria][periodo].update(tokens)

        return resultado

    def cambios_frecuencia(self):
        terminos_periodo = self.terminos_por_categoria_y_periodo()
        periodos = sorted(self.df["periodo"].unique())

        primero = periodos[0]
        ultimo = periodos[-1]

        cambios = {}

        for categoria, datos_periodo in terminos_periodo.items():
            inicial = datos_periodo.get(primero, Counter())
            final = datos_periodo.get(ultimo, Counter())

            vocabulario = set(inicial.keys()) | set(final.keys())
            diffs = []

            for termino in vocabulario:
                cambio = final[termino] - inicial[termino]
                diffs.append((termino, inicial[termino], final[termino], cambio))

            aumentan = sorted(diffs, key=lambda x: x[3], reverse=True)[:5]
            disminuyen = sorted(diffs, key=lambda x: x[3])[:5]

            cambios[categoria] = {
                "primer_periodo": primero,
                "ultimo_periodo": ultimo,
                "aumentan": aumentan,
                "disminuyen": disminuyen
            }

        return cambios

    def detectar_picos_caidas(self):
        tabla = self.tabla_conteo_por_periodo()
        hallazgos = []

        for categoria in tabla.columns:
            serie = tabla[categoria]
            max_periodo = serie.idxmax()
            max_valor = serie.max()
            min_periodo = serie.idxmin()
            min_valor = serie.min()

            titulo_ejemplo = self.df[
                (self.df["periodo"] == max_periodo) &
                (self.df["categoria_predicha"] == categoria)
            ]["titulo"]

            ejemplo = titulo_ejemplo.iloc[0] if not titulo_ejemplo.empty else "Sin ejemplo"

            hallazgos.append({
                "categoria": categoria,
                "pico_periodo": max_periodo,
                "pico_valor": int(max_valor),
                "caida_periodo": min_periodo,
                "caida_valor": int(min_valor),
                "titulo_apoyo": ejemplo
            })

        return hallazgos

    def exportar_tabla(self, archivo="tabla_tendencias.csv"):
        tabla = self.tabla_conteo_por_periodo()
        tabla.to_csv(archivo, encoding="utf-8")
        return archivo

    def generar_grafica(self, archivo="grafica_tendencias.png"):
        tabla = self.tabla_conteo_por_periodo()
        tabla.plot(marker="o")
        plt.title("Tendencias por tema en el corpus SIMANW")
        plt.xlabel("Periodo mensual")
        plt.ylabel("Número de noticias")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(archivo)
        plt.close()
        return archivo

    def conclusion(self):
        tabla = self.tabla_conteo_por_periodo()
        hallazgos = self.detectar_picos_caidas()

        categoria_dominante = tabla.sum().idxmax()
        total_dominante = tabla.sum().max()

        texto = (
            "Conclusión del análisis temporal:\n\n"
            f"El análisis se realizó con granularidad mensual. Esta decisión permite "
            f"observar la evolución de los temas sin fragmentar excesivamente el corpus. "
            f"En el periodo analizado, la categoría con mayor presencia fue "
            f"'{categoria_dominante}', con {total_dominante} noticias acumuladas. "
            f"Esto indica que dicho tema mantuvo una presencia constante dentro del corpus.\n\n"
            "También se identificaron cambios relevantes entre periodos. Algunos temas "
            "presentan picos asociados a noticias específicas, lo cual sugiere que ciertos "
            "eventos pueden aumentar temporalmente la atención mediática. Por ejemplo, "
        )

        if hallazgos:
            h = hallazgos[0]
            texto += (
                f"la categoría '{h['categoria']}' alcanzó un pico en {h['pico_periodo']} "
                f"con apoyo en el título: \"{h['titulo_apoyo']}\". "
            )

        texto += (
            "\n\nEn términos generales, el módulo permite detectar qué temas ganan o pierden "
            "presencia, comparar categorías y observar expresiones que aumentan o disminuyen "
            "entre el primer y último periodo. Esta información puede utilizarse para alimentar "
            "reportes automáticos, mejorar el sistema de búsqueda y orientar recomendaciones "
            "temáticas dentro del SIMANW."
        )

        return texto


print("=== AC-9: Línea de Tiempo y Tendencias por Tema ===\n")

analizador = AnalizadorTendencias(noticias)

print("Granularidad elegida:")
print(analizador.justificar_granularidad())

print("\n--- Tabla de conteo por periodo ---")
tabla = analizador.tabla_conteo_por_periodo()
print(tabla)

print("\n--- Términos que aumentan o disminuyen ---")
cambios = analizador.cambios_frecuencia()

for categoria, info in cambios.items():
    print(f"\nCategoría: {categoria}")
    print(f"Primer periodo: {info['primer_periodo']} | Último periodo: {info['ultimo_periodo']}")

    print("Aumentan:")
    for termino, inicial, final, cambio in info["aumentan"]:
        print(f"  {termino}: {inicial} → {final} ({cambio:+})")

    print("Disminuyen:")
    for termino, inicial, final, cambio in info["disminuyen"]:
        print(f"  {termino}: {inicial} → {final} ({cambio:+})")

print("\n--- Picos y caídas detectadas ---")
for h in analizador.detectar_picos_caidas():
    print(
        f"{h['categoria']}: pico en {h['pico_periodo']} "
        f"({h['pico_valor']} noticia/s), caída en {h['caida_periodo']} "
        f"({h['caida_valor']} noticia/s)"
    )
    print(f"  Título de apoyo: {h['titulo_apoyo']}")

archivo_tabla = analizador.exportar_tabla()
archivo_grafica = analizador.generar_grafica()

print("\nArchivos generados:")
print(f"- {archivo_tabla}")
print(f"- {archivo_grafica}")

print("\n--- Conclusión ---")
print(analizador.conclusion())