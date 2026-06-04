import json
from modules.nlp.quality import ControlCalidadCorpus, cargar_json, guardar_json
from modules.nlp.pipeline import PipelineNLP
from modules.classification.classifier import ClasificadorNoticias
from modules.classification.sentiment import AnalizadorSentimientos
from modules.search.engine import MotorBusqueda
from modules.search.alerts import SistemaAlertas
from modules.chatbot.assistant import ChatbotSIMANW
from modules.semantic.knowledge_graph import KnowledgeGraphSIMANW
from modules.reports.report_generator import GeneradorReportes, guardar_texto
from pathlib import Path

from modules.crawler.crawler import RastreadorNoticias

def cargar_version():
    ruta = Path("config/version.json")

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def mostrar_menu():
    print("\n==============================")
    print(" SIMANW")
    print("==============================")
    print("1. Rastrear noticias")
    print("2. Procesar corpus")
    print("3. Clasificar y analizar sentimiento")
    print("4. Buscar noticias")
    print("5. Alertas")
    print("6. Chatbot / Q&A")
    print("7. Knowledge Graph")
    print("8. Reportes")
    print("0. Salir")


def ejecutar_rastreo():
    rastreador = RastreadorNoticias(
        modo_demo=True,
        max_paginas=4
    )

    noticias = rastreador.rastrear()
    ruta = rastreador.guardar_json()

    print("\nRastreo completado.")
    print(f"Noticias extraídas: {len(noticias)}")
    print(f"Archivo generado: {ruta}")

def ejecutar_procesamiento():
    ruta_raw = Path("data/raw/noticias_raw.json")

    if not ruta_raw.exists():
        print("\nNo existe data/raw/noticias_raw.json")
        print("Primero ejecuta la opción 1: Rastrear noticias.")
        return

    noticias = cargar_json(ruta_raw)

    print("\nEjecutando control de calidad...")

    control = ControlCalidadCorpus(min_cuerpo=40, umbral_similitud=0.90)
    noticias_limpias = control.depurar(noticias)
    informe = control.generar_informe(len(noticias))

    guardar_json("data/processed/noticias_limpias.json", noticias_limpias)
    guardar_json("outputs/reports/informe_calidad_corpus.json", informe)

    print(f"Registros originales: {informe['total_registros']}")
    print(f"Registros válidos: {informe['registros_validos']}")
    print(f"Registros descartados: {informe['registros_descartados']}")

    print("\nEjecutando procesamiento NLP...")

    pipeline = PipelineNLP()
    noticias_procesadas = pipeline.procesar_noticias(noticias_limpias)
    stats = pipeline.estadisticas_corpus(noticias_procesadas)

    guardar_json("data/processed/noticias_procesadas.json", noticias_procesadas)
    guardar_json("outputs/reports/estadisticas_nlp.json", stats)

    print("\nProcesamiento completado.")
    print(f"Documentos procesados: {stats['total_documentos']}")
    print(f"Tokens totales: {stats['total_tokens']}")
    print(f"Vocabulario total: {stats['vocabulario_total']}")
    print("Archivos generados:")
    print("- data/processed/noticias_limpias.json")
    print("- data/processed/noticias_procesadas.json")
    print("- outputs/reports/informe_calidad_corpus.json")
    print("- outputs/reports/estadisticas_nlp.json")

def ejecutar_analisis():
    ruta_procesadas = Path("data/processed/noticias_procesadas.json")

    if not ruta_procesadas.exists():
        print("\nNo existe data/processed/noticias_procesadas.json")
        print("Primero ejecuta la opción 2: Procesar corpus.")
        return

    noticias = cargar_json(ruta_procesadas)

    print("\nEjecutando clasificación automática...")

    clasificador = ClasificadorNoticias()
    noticias_clasificadas, reporte_clasificacion = clasificador.clasificar_noticias(noticias)

    guardar_json("outputs/reports/reporte_clasificacion.json", reporte_clasificacion)

    print(f"Noticias clasificadas: {reporte_clasificacion['total_clasificadas']}")
    print(f"Categorías: {reporte_clasificacion['categorias']}")
    print(f"Accuracy CV: {reporte_clasificacion['accuracy_cv']:.3f}")

    print("\nEjecutando análisis de sentimiento...")

    analizador = AnalizadorSentimientos()
    noticias_analizadas, reporte_sentimiento = analizador.analizar_noticias(noticias_clasificadas)

    guardar_json("data/processed/noticias_analizadas.json", noticias_analizadas)
    guardar_json("outputs/reports/reporte_sentimiento.json", reporte_sentimiento)

    print(f"Noticias analizadas: {reporte_sentimiento['total_analizadas']}")
    print(f"Distribución: {reporte_sentimiento['distribucion_sentimiento']}")
    print(f"Tono general: {reporte_sentimiento['tono_general']}")
    print("Archivos generados:")
    print("- data/processed/noticias_analizadas.json")
    print("- outputs/reports/reporte_clasificacion.json")
    print("- outputs/reports/reporte_sentimiento.json")

def ejecutar_busqueda():
    ruta_analizadas = Path("data/processed/noticias_analizadas.json")

    if not ruta_analizadas.exists():
        print("\nNo existe data/processed/noticias_analizadas.json")
        print("Primero ejecuta la opción 3: Clasificar y analizar sentimiento.")
        return

    noticias = cargar_json(ruta_analizadas)

    motor = MotorBusqueda()
    motor.indexar(noticias)

    info = motor.info_indice()

    print("\nMotor de búsqueda listo.")
    print(f"Documentos indexados: {info['documentos_indexados']}")
    print(f"Términos en índice: {info['terminos_en_indice']}")

    consulta = input("\nEscribe tu búsqueda: ")

    resultados = motor.buscar_vectorial(consulta, top_k=5)

    print("\nResultados:")

    if not resultados:
        print("No se encontraron resultados relevantes.")
        return

    for r in resultados:
        print(f"\n[{r['relevancia']:.3f}] {r['titulo']}")
        print(f"Categoría: {r['categoria']} | Sentimiento: {r['sentimiento']}")
        print(f"Resumen: {r['snippet']}")
        print(f"URL: {r['url']}")

def ejecutar_alertas():
    ruta_analizadas = Path("data/processed/noticias_analizadas.json")

    if not ruta_analizadas.exists():
        print("\nNo existe data/processed/noticias_analizadas.json")
        print("Primero ejecuta la opción 3: Clasificar y analizar sentimiento.")
        return

    noticias = cargar_json(ruta_analizadas)

    sistema_alertas = SistemaAlertas()
    sistema_alertas.cargar_consultas_base()

    alertas = sistema_alertas.revisar(noticias)
    ruta = sistema_alertas.guardar()

    print("\nSistema de alertas ejecutado.")
    print(f"Consultas guardadas: {len(sistema_alertas.consultas_guardadas)}")
    print(f"Alertas generadas: {len(alertas)}")

    if alertas:
        print("\nAlertas:")
        for a in alertas:
            print(f"- {a['consulta_nombre']} → {a['titulo']}")

    print(f"\nHistorial guardado en: {ruta}")

def ejecutar_chatbot():
    ruta_analizadas = Path("data/processed/noticias_analizadas.json")

    if not ruta_analizadas.exists():
        print("\nNo existe data/processed/noticias_analizadas.json")
        print("Primero ejecuta la opción 3: Clasificar y analizar sentimiento.")
        return

    noticias = cargar_json(ruta_analizadas)

    motor = MotorBusqueda()
    motor.indexar(noticias)

    chatbot = ChatbotSIMANW(noticias, motor)

    print("\nChatbot SIMANW iniciado.")
    print("Escribe 'salir' para volver al menú.")

    while True:
        pregunta = input("\nUsuario: ")

        if pregunta.lower().strip() == "salir":
            stats = chatbot.estadisticas_sesion()
            print("\nResumen de sesión:")
            print(f"Interacciones: {stats['interacciones']}")
            print(f"Temas de interés: {stats['temas_interes']}")
            print(f"Tipos de respuesta: {stats['tipos_respuesta']}")
            break

        respuesta, tipo, confianza = chatbot.responder(pregunta)

        print(f"\nBot [{tipo}][{confianza:.2f}]:")
        print(respuesta)

def ejecutar_knowledge_graph():
    ruta_analizadas = Path("data/processed/noticias_analizadas.json")

    if not ruta_analizadas.exists():
        print("\nNo existe data/processed/noticias_analizadas.json")
        print("Primero ejecuta la opción 3: Clasificar y analizar sentimiento.")
        return

    noticias = cargar_json(ruta_analizadas)

    kg = KnowledgeGraphSIMANW()
    kg.construir_desde_noticias(noticias)
    kg.exportar()

    consultas = kg.consultas_demo()

    reporte = {
        "total_noticias": len(noticias),
        "total_triples": kg.total_triples(),
        "archivos_generados": [
            "data/rdf/simanw_kg.ttl",
            "data/rdf/simanw_kg.jsonld"
        ],
        "consultas_demo": {
            "categorias": len(consultas["categorias"]),
            "sentimiento_negativo": len(consultas["sentimiento_negativo"]),
            "enlaces_externos": len(consultas["enlaces_externos"])
        }
    }

    guardar_json("outputs/reports/reporte_kg.json", reporte)

    print("\nKnowledge Graph generado.")
    print(f"Noticias integradas: {len(noticias)}")
    print(f"Total de triples: {kg.total_triples()}")

    print("\nConsulta SPARQL 1: Distribución por categoría")
    for row in consultas["categorias"]:
        print(f"- {row.categoria}: {row.total}")

    print("\nConsulta SPARQL 2: Noticias con sentimiento negativo")
    for row in consultas["sentimiento_negativo"]:
        print(f"- [{float(row.score):+.3f}] {row.titulo}")

    print("\nConsulta SPARQL 3: Enlaces externos")
    for row in consultas["enlaces_externos"]:
        local = str(row.local).split("/")[-1]
        externo = str(row.externo).split("/")[-1]
        print(f"- {local} → {externo} ({row.etiqueta})")

    print("\nArchivos generados:")
    print("- data/rdf/simanw_kg.ttl")
    print("- data/rdf/simanw_kg.jsonld")
    print("- outputs/reports/reporte_kg.json")

def ejecutar_reportes():
    ruta_analizadas = Path("data/processed/noticias_analizadas.json")
    ruta_reporte_kg = Path("outputs/reports/reporte_kg.json")

    if not ruta_analizadas.exists():
        print("\nNo existe data/processed/noticias_analizadas.json")
        print("Primero ejecuta la opción 3: Clasificar y analizar sentimiento.")
        return

    noticias = cargar_json(ruta_analizadas)

    total_triples = 0

    if ruta_reporte_kg.exists():
        reporte_kg = cargar_json(ruta_reporte_kg)
        total_triples = reporte_kg.get("total_triples", 0)

    generador = GeneradorReportes(noticias)

    reporte = generador.generar_reporte_texto(total_triples=total_triples)
    manifiesto = generador.generar_manifiesto(total_triples=total_triples)

    guardar_texto("outputs/reports/reporte_final_simanw.txt", reporte)
    guardar_json("outputs/reports/manifiesto_ejecucion.json", manifiesto)

    print("\nReporte final generado.")
    print("Archivos generados:")
    print("- outputs/reports/reporte_final_simanw.txt")
    print("- outputs/reports/manifiesto_ejecucion.json")

def main():
    version = cargar_version()

    print(f"\n{version['project']} v{version['version']}")
    print(version["description"])

    while True:
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            ejecutar_rastreo()

        elif opcion == "2":
            ejecutar_procesamiento()

        elif opcion == "3":
            ejecutar_analisis()

        elif opcion == "4":
            ejecutar_busqueda()

        elif opcion == "5":
            ejecutar_alertas()

        elif opcion == "6":
            ejecutar_chatbot()

        elif opcion == "7":
            ejecutar_knowledge_graph()

        elif opcion == "8":
            ejecutar_reportes()

        elif opcion == "0":
            print("Hasta luego.")
            break

        else:
            print(f"\n[MÓDULO {opcion} EN CONSTRUCCIÓN]")


if __name__ == "__main__":
    main()