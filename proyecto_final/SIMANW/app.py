import json
import plotly.express as px
from pathlib import Path

import streamlit as st
import pandas as pd

from modules.analytics.timeline import AnalizadorTemporal
from modules.crawler.crawler import RastreadorNoticias
from modules.crawler.paginated import RastreadorPaginado
from modules.crawler.rss_reader import LectorRSS
from modules.nlp.quality import ControlCalidadCorpus, cargar_json, guardar_json
from modules.nlp.pipeline import PipelineNLP
from modules.nlp.discourse import AnalisisDiscurso
from modules.classification.classifier import ClasificadorNoticias
from modules.classification.sentiment import AnalizadorSentimientos
from modules.classification.model_selector import SelectorModelo
from modules.search.engine import MotorBusqueda
from modules.search.alerts import SistemaAlertas
from modules.search.evaluator import evaluar_motor_con_corpus
from modules.search.hybrid_search import BuscadorHibrido
from modules.chatbot.assistant import ChatbotSIMANW
from modules.chatbot.ads import DetectorTemasPublicidad
from modules.semantic.knowledge_graph import KnowledgeGraphSIMANW
from modules.semantic.open_data import ConectorDatosAbiertos
from modules.semantic.external_sparql import consultas_documentadas, ejecutar_consulta_wikidata
from modules.semantic.shacl_validator import ValidadorSHACL
from modules.social.thread_analyzer import AnalizadorHiloDiscusion, hilo_demo
from modules.reports.report_generator import GeneradorReportes, guardar_texto
from assets.components import (
    cargar_css,
    card,
    noticia_card,
    chat_bubble,
    color_categoria,
    color_sentimiento,
    tabla_html
)


st.set_page_config(
    page_title="SIMANW",
    layout="wide"
)

cargar_css()


def existe(ruta):
    return Path(ruta).exists()


def cargar_seguro(ruta):
    if existe(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def cargar_noticias_demo():
    ruta = Path("data/raw/noticias_base.json")

    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    rastreador = RastreadorNoticias(modo_demo=True, max_paginas=4)
    noticias = rastreador.rastrear()
    rastreador.guardar_json()

    return noticias


def cargar_noticias_rss():
    feeds = [
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

    try:
        lector = LectorRSS(feeds)
        noticias = lector.leer()
        lector.guardar_json("data/raw/noticias_rss.json")
        return noticias

    except Exception as e:
        print(f"Error cargando RSS: {e}")
        return []

def ejecutar_pipeline():
    noticias_demo = cargar_noticias_demo()
    noticias_rss = cargar_noticias_rss()

    noticias = noticias_demo + noticias_rss

    guardar_json("data/raw/noticias_raw.json", noticias)

    control = ControlCalidadCorpus()
    limpias = control.depurar(noticias)
    informe = control.generar_informe(len(noticias))

    guardar_json("data/processed/noticias_limpias.json", limpias)
    guardar_json("outputs/reports/informe_calidad_corpus.json", informe)

    pipeline = PipelineNLP()
    procesadas = pipeline.procesar_noticias(limpias)
    stats = pipeline.estadisticas_corpus(procesadas)

    guardar_json("data/processed/noticias_procesadas.json", procesadas)
    guardar_json("outputs/reports/estadisticas_nlp.json", stats)

    clasificador = ClasificadorNoticias()
    clasificadas, reporte_clasificacion = clasificador.clasificar_noticias(procesadas)

    textos_modelos = [
        f"{n['titulo']} {n['cuerpo']}"
        for n in procesadas
    ]

    etiquetas_modelos = [
        n.get("categoria_original", "general")
        for n in procesadas
    ]

    reporte_clasificacion["comparacion_modelos"] = {}
    reporte_clasificacion["mejor_modelo_multimodelo"] = "No evaluado"

    if len(set(etiquetas_modelos)) >= 2 and len(etiquetas_modelos) >= 6:
        try:
            selector = SelectorModelo()
            resultados_modelos = selector.evaluar_todos(
                textos_modelos,
                etiquetas_modelos,
                cv_folds=2
            )

            reporte_clasificacion["comparacion_modelos"] = resultados_modelos
            reporte_clasificacion["mejor_modelo_multimodelo"] = selector.obtener_mejor_modelo()

        except Exception as e:
            reporte_clasificacion["comparacion_modelos"] = {
                "error": str(e)
            }

    guardar_json("outputs/reports/reporte_clasificacion.json", reporte_clasificacion)

    analizador = AnalizadorSentimientos()
    analizadas, reporte_sentimiento = analizador.analizar_noticias(clasificadas)

    guardar_json("data/processed/noticias_analizadas.json", analizadas)
    guardar_json("outputs/reports/reporte_sentimiento.json", reporte_sentimiento)

    kg = KnowledgeGraphSIMANW()
    kg.construir_desde_noticias(analizadas)

    # kg.agregar_noticia_incompleta_prueba()

    conector = ConectorDatosAbiertos(kg)
    conector.cargar_datasets_demo()

    datasets = conector.consultar_datos()
    enlaces_creados = conector.crear_enlaces_semanticos()
    enlaces_datos = conector.enlazar_noticias_con_datos()

    kg.exportar()

    guardar_json("outputs/reports/reporte_kg.json", {
        "total_noticias": len(analizadas),
        "total_triples": kg.total_triples(),
        "datasets_abiertos": len(datasets),
        "enlaces_noticias_datasets": len(enlaces_datos),
        "enlaces_creados_detalle": enlaces_creados
    })

    generador = GeneradorReportes(analizadas)
    reporte = generador.generar_reporte_texto(total_triples=kg.total_triples())
    manifiesto = generador.generar_manifiesto(total_triples=kg.total_triples())

    guardar_texto("outputs/reports/reporte_final_simanw.txt", reporte)
    guardar_json("outputs/reports/manifiesto_ejecucion.json", manifiesto)

    return len(analizadas)


st.sidebar.title("SIMANW")
st.sidebar.caption("Sistema Inteligente de Monitoreo y Análisis de Noticias Web")

seccion = st.sidebar.radio(
    "Navegación",
    [
        "Inicio",
        "Buscador",
        "Rastreo paginado",
        "Tendencias",
        "Chatbot",
        "Alertas",
        "Knowledge Graph",
        "Análisis de hilo",
        "Reportes"
    ]
)


noticias = cargar_seguro("data/processed/noticias_analizadas.json")


if seccion == "Inicio":
    st.title("SIMANW")
    st.subheader("Sistema Inteligente de Monitoreo y Análisis de Noticias Web")

    st.markdown("### Actualización del corpus")

    col_update, col_info = st.columns([1, 2])

    with col_update:
        if st.button("Ejecutar pipeline completo"):
            with st.spinner("Procesando SIMANW..."):
                total = ejecutar_pipeline()
            st.success(f"Pipeline completado. Noticias analizadas: {total}")
            st.rerun()

    with col_info:
        st.info(
            "Este proceso actualiza el corpus, limpia datos, ejecuta NLP, "
            "clasifica noticias, calcula sentimiento, genera el grafo RDF y reportes."
        )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    total = len(noticias)
    categorias = len(set(n.get("categoria_predicha", "general") for n in noticias)) if noticias else 0
    positivos = sum(1 for n in noticias if n.get("sentimiento", {}).get("etiqueta") == "positivo")
    negativos = sum(1 for n in noticias if n.get("sentimiento", {}).get("etiqueta") == "negativo")

    with col1:
        card("Noticias", total, "Corpus analizado")
    with col2:
        card("Categorías", categorias, "Temas detectados")
    with col3:
        card("Positivas", positivos, "Sentimiento positivo")
    with col4:
        card("Negativas", negativos, "Sentimiento negativo")

    st.markdown("---")

    if noticias:
        st.subheader("Últimas noticias procesadas")
        df = pd.DataFrame([
            {
                "Título": n["titulo"],
                "Categoría": n.get("categoria_predicha", n.get("categoria_original", "?")),
                "Sentimiento": n.get("sentimiento", {}).get("etiqueta", "?"),
                "Fecha": n.get("fecha", "?")
            }
            for n in noticias
        ])
        tabla_html(df)
    else:
        st.info("Aún no hay corpus procesado. Ejecuta el pipeline completo desde esta pantalla.")


elif seccion == "Buscador":
    st.title("Buscador inteligente")

    if not noticias:
        st.warning("Primero actualiza el corpus.")
    else:
        consulta = st.text_input(
            "Buscar noticias",
            placeholder="Ejemplo: inteligencia artificial, salud, videojuegos, economía"
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            ia_vectorial = st.toggle("IA Vectorial", value=True)
            busqueda_hibrida = st.toggle("Búsqueda híbrida", value=True)
            usar_rss = st.toggle("Consultar RSS si no hay resultados locales", value=True)
            usar_web = st.toggle("Consultar web externa si RSS no encuentra resultados", value=False)

        with col_b:
            top_k = st.slider("Número de resultados", 1, 15, 5)

        with col_c:
            umbral = st.slider("Similitud mínima", 0.0, 1.0, 0.10, 0.05)

        modo_booleano = st.selectbox(
            "Modo booleano",
            ["AND", "OR"],
            help="AND exige que aparezcan todos los términos. OR acepta que aparezca al menos uno."
        )

        st.markdown("---")
        st.subheader("Evaluación formal del motor")

        if st.button("Evaluar motor de búsqueda"):
            motor_eval = MotorBusqueda()
            motor_eval.indexar(noticias)

            resultados_eval, map_score = evaluar_motor_con_corpus(motor_eval, noticias)

            st.write(f"MAP general: **{map_score:.3f}**")

            df_eval = pd.DataFrame([
                {
                    "Consulta": r["consulta"],
                    "Precision": round(r["precision"], 3),
                    "Recall": round(r["recall"], 3),
                    "F1": round(r["f1"], 3),
                    "AP": round(r["average_precision"], 3),
                    "Relevantes": len(r["relevantes"]),
                    "Recuperados": len(r["recuperados"])
                }
                for r in resultados_eval
            ])

            tabla_html(df_eval)

        if st.button("Buscar"):
            if not consulta.strip():
                st.warning("Escribe una consulta primero.")
            else:
                motor = MotorBusqueda()
                motor.indexar(noticias)

                if ia_vectorial:
                    if busqueda_hibrida:
                        buscador_hibrido = BuscadorHibrido(motor, noticias)

                        resultados, fuente_resultados = buscador_hibrido.buscar(
                            consulta=consulta,
                            top_k=top_k,
                            umbral=umbral,
                            usar_rss=usar_rss,
                            usar_web=usar_web
                        )

                        st.info(f"Fuente de resultados: {fuente_resultados}")

                    else:
                        resultados_base = motor.buscar_vectorial(
                            consulta,
                            top_k=len(noticias)
                        )

                        resultados = [
                            r for r in resultados_base
                            if r["relevancia"] >= umbral
                        ]

                        resultados = resultados[:top_k]

                else:
                    ids = motor.buscar_booleana(consulta, modo=modo_booleano)

                    resultados = [
                        {
                            "titulo": noticias[i]["titulo"],
                            "categoria": noticias[i].get("categoria_predicha", noticias[i].get("categoria_original", "?")),
                            "sentimiento": noticias[i].get("sentimiento", {}).get("etiqueta", "?"),
                            "snippet": noticias[i]["cuerpo"][:160] + "...",
                            "relevancia": 1.0,
                            "url": noticias[i].get("url", "")
                        }
                        for i in ids[:top_k]
                    ]

                st.subheader("Resultados")

                st.write(f"Resultados encontrados: **{len(resultados)}**")

                if not resultados:
                    st.info(
                        "No se encontraron resultados con esos criterios. "
                        "Prueba bajar la similitud mínima, activar IA Vectorial o usar menos palabras."
                    )
                else:
                    for r in resultados:
                        noticia_card(
                            titulo=r["titulo"],
                            snippet=r["snippet"],
                            categoria=r["categoria"],
                            sentimiento=r["sentimiento"],
                            similitud=r["relevancia"] * 100,
                            fuente=r.get("fuente"),
                            url=r.get("url")
                        )

elif seccion == "Rastreo paginado":
    st.title("Rastreo paginado")

    st.write(
        "Este módulo demuestra el rastreo con paginación, control de páginas, "
        "delay entre peticiones y verificación de robots.txt en modo producción."
    )

    max_paginas = st.slider("Páginas a rastrear", 1, 6, 4)
    delay = st.slider("Delay entre peticiones", 1, 10, 3)

    if st.button("Ejecutar rastreo paginado"):
        rastreador = RastreadorPaginado(
            url_base="https://ejemplo-noticias.com/ultimas",
            selector_articulos="article",
            selector_siguiente="a.next-page",
            delay=delay,
            max_paginas=max_paginas,
            modo_demo=True
        )

        resultados = rastreador.rastrear()
        total = rastreador.guardar_json("outputs/reports/ac1_rastreo_paginado.json")

        st.success(f"Rastreo completado. Noticias extraídas: {total}")

        tabla_html(pd.DataFrame(resultados))

elif seccion == "Tendencias":
    st.title("Tendencias del corpus")

    if not noticias:
        st.warning("Primero actualiza el corpus.")
    else:
        df = pd.DataFrame(noticias)

        st.subheader("Distribución por categoría")

        if "categoria_predicha" in df.columns:
            conteo = df["categoria_predicha"].value_counts()

            conteo_df = pd.DataFrame({
                "Categoría": conteo.index,
                "Total": conteo.values
            })

            fig = px.bar(
                conteo_df,
                x="Categoría",
                y="Total",
                color="Categoría",
                color_discrete_map={
                    "tecnologia": "#4A90E2",
                    "ciencia": "#4CAF7D",
                    "videojuegos": "#1F4E79",
                    "salud": "#E07A5F",
                    "economia": "#D4A017",
                    "politica": "#8E5EA2",
                    "general": "#7A7A7A"
                }
            )

            fig.update_layout(
                paper_bgcolor="#F7F1E8",
                plot_bgcolor="#F7F1E8",
                font_color="#2B211E"
            )

            st.plotly_chart(fig, use_container_width=True)
            tabla_html(conteo_df)

        st.subheader("Distribución de sentimiento")

        if "sentimiento" in df.columns:
            df["sentimiento_etiqueta"] = df["sentimiento"].apply(
                lambda x: x.get("etiqueta", "?") if isinstance(x, dict) else "?"
            )

            sentimiento_conteo = df["sentimiento_etiqueta"].value_counts()

            sent_df = pd.DataFrame({
                "Sentimiento": sentimiento_conteo.index,
                "Total": sentimiento_conteo.values
            })

            fig_sent = px.bar(
                sent_df,
                x="Sentimiento",
                y="Total",
                color="Sentimiento",
                color_discrete_map={
                    "positivo": "#2EAD6B",
                    "negativo": "#C0392B",
                    "neutral": "#7F8C8D",
                    "?": "#7F8C8D"
                }
            )

            fig_sent.update_layout(
                paper_bgcolor="#F7F1E8",
                plot_bgcolor="#F7F1E8",
                font_color="#2B211E"
            )

            st.plotly_chart(fig_sent, use_container_width=True)
            tabla_html(sent_df)

    st.markdown("---")
    st.subheader("Análisis estadístico del corpus")
    
    texto_corpus = " ".join(
        f"{n['titulo']} {n['cuerpo']}"
        for n in noticias
    )
    
    analizador = AnalisisDiscurso()
    analisis = analizador.analizar(texto_corpus)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        card("Palabras", analisis["palabras_totales"], "Total del corpus")
    with col_b:
        card("Vocabulario", analisis["vocabulario_unico"], "Términos únicos")
    with col_c:
        card(
            "Riqueza léxica",
            f"{analisis['riqueza_lexica_global']:.3f}",
            "Diversidad del vocabulario"
        )
    
    st.subheader("Bigramas frecuentes")
    tabla_html(pd.DataFrame([
        {"Bigrama": " ".join(b), "Frecuencia": f}
        for b, f in analisis["top_bigramas"]
    ]))
    
    st.subheader("Trigramas frecuentes")
    tabla_html(pd.DataFrame([
        {"Trigrama": " ".join(t), "Frecuencia": f}
        for t, f in analisis["top_trigramas"]
    ]))
    
    st.subheader("Posibles entidades nombradas")
    tabla_html(pd.DataFrame([
        {"Entidad": e, "Frecuencia": f}
        for e, f in analisis["posibles_entidades"]
    ]))

    st.markdown("---")
    st.subheader("Línea temporal del corpus")

    temporal = AnalizadorTemporal(noticias)

    timeline = temporal.construir_timeline()

    if not timeline.empty:

        fig_time = px.line(
            timeline,
            x="periodo",
            y="total",
            color=timeline.columns[1],
            markers=True
        )

        fig_time.update_layout(
            paper_bgcolor="#F7F1E8",
            plot_bgcolor="#F7F1E8"
        )

        st.plotly_chart(
            fig_time,
            use_container_width=True
        )

        st.subheader("Resumen exportable")

        tabla_html(timeline)

        st.download_button(
            "Descargar CSV",
            timeline.to_csv(index=False),
            file_name="timeline.csv"
        )

    st.subheader("Picos detectados")

    picos = temporal.detectar_picos()

    tabla_html(pd.DataFrame(picos))


elif seccion == "Chatbot":
    st.title("Chatbot SIMANW")

    if not noticias:
        st.warning("Primero actualiza el corpus.")
    else:
        corpus_id = len(noticias)

        if "chat_corpus_id" not in st.session_state:
            st.session_state.chat_corpus_id = corpus_id

        if st.session_state.chat_corpus_id != corpus_id:
            st.session_state.chat_historial = []
            if "chatbot_simanw" in st.session_state:
                del st.session_state.chatbot_simanw
            st.session_state.chat_corpus_id = corpus_id

        motor = MotorBusqueda()
        motor.indexar(noticias)

        if "chatbot_simanw" not in st.session_state:
            st.session_state.chatbot_simanw = ChatbotSIMANW(noticias, motor)

        if "chat_historial" not in st.session_state:
            st.session_state.chat_historial = []

        if "detector_ads" not in st.session_state:
            st.session_state.detector_ads = DetectorTemasPublicidad()

        if st.button("Reiniciar conversación"):
            for key in ["chatbot_simanw", "chat_historial", "chat_corpus_id", "detector_ads", "ultimo_anuncio"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        pregunta = st.chat_input("Pregunta algo sobre las noticias...")

        if pregunta:
            chatbot = st.session_state.chatbot_simanw
            respuesta, tipo, confianza = chatbot.responder(pregunta)

            st.session_state.chat_historial.append(("Usuario", pregunta))
            st.session_state.chat_historial.append(
                ("SIMANW", f"[{tipo}][{confianza:.2f}] {respuesta}")
            )

            detector = st.session_state.detector_ads
            detector.agregar_mensaje("Usuario", pregunta)
            tema_ads, confianza_ads = detector.detectar_tema()
            publicidad = detector.obtener_publicidad(tema_ads)

            st.session_state.ultimo_anuncio = {
                "tema": tema_ads,
                "confianza": confianza_ads,
                "publicidad": publicidad
            }

        for rol, mensaje in st.session_state.chat_historial:
            chat_bubble(rol, mensaje)

        if "ultimo_anuncio" in st.session_state:
            anuncio = st.session_state.ultimo_anuncio

            st.markdown("---")
            st.subheader("Tema detectado para publicidad dirigida")

            st.write(f"Tema dominante: **{anuncio['tema']}**")
            st.write(f"Confianza: **{anuncio['confianza']:.3f}**")
            st.info(f"Publicidad sugerida: {anuncio['publicidad']}")

elif seccion == "Alertas":
    st.title("Alertas por consultas guardadas")

    if not noticias:
        st.warning("Primero actualiza el corpus.")
    else:
        st.write(
            "Las alertas se activan cuando una noticia del corpus coincide con una consulta guardada."
        )

        sistema_alertas = SistemaAlertas()
        sistema_alertas.cargar_consultas_base()

        st.subheader("Consultas guardadas")

        consultas_df = pd.DataFrame(sistema_alertas.consultas_guardadas)
        tabla_html(consultas_df)

        historial_path = Path("outputs/alerts/historial_alertas.json")

        if historial_path.exists():
            historial = json.loads(historial_path.read_text(encoding="utf-8"))
        else:
            historial = []

        st.subheader("Historial de alertas")

        if historial:
            tabla_html(pd.DataFrame(historial))
        else:
            st.info("Todavía no hay alertas registradas.")

        st.markdown("---")

        if st.button("Revisar alertas del corpus actual"):
            alertas = sistema_alertas.revisar(noticias)

            nuevas = []

            claves_historial = {
                (a["consulta_id"], a["noticia_id"])
                for a in historial
            }

            for alerta in alertas:
                clave = (alerta["consulta_id"], alerta["noticia_id"])

                if clave not in claves_historial:
                    nuevas.append(alerta)
                    historial.append(alerta)

            Path("outputs/alerts").mkdir(parents=True, exist_ok=True)

            with open(historial_path, "w", encoding="utf-8") as f:
                json.dump(historial, f, ensure_ascii=False, indent=2)

            if nuevas:
                st.success(f"Alertas nuevas generadas: {len(nuevas)}")
                st.dataframe(pd.DataFrame(nuevas), use_container_width=True)
            else:
                st.info("No hay alertas nuevas. Las coincidencias ya estaban registradas.")


elif seccion == "Knowledge Graph":
    st.title("Knowledge Graph")

    ttl = Path("data/rdf/simanw_kg.ttl")
    jsonld = Path("data/rdf/simanw_kg.jsonld")
    reporte_kg = cargar_seguro("outputs/reports/reporte_kg.json")

    if reporte_kg:
        col1, col2 = st.columns(2)
        with col1:
            card("Triples", reporte_kg.get("total_triples", 0), "RDF generado")
        with col2:
            card("Noticias", reporte_kg.get("total_noticias", 0), "Recursos incluidos")

    st.markdown("---")
    st.subheader("Datos abiertos integrados")

    if reporte_kg:
        col_a, col_b = st.columns(2)

        with col_a:
            card(
                "Datasets abiertos",
                reporte_kg.get("datasets_abiertos", 0),
                "Fuentes públicas simuladas"
            )

        with col_b:
            card(
                "Enlaces semánticos",
                reporte_kg.get("enlaces_noticias_datasets", 0),
                "Noticias vinculadas a datasets"
            )

    if ttl.exists():
        st.success("Archivo Turtle generado.")
        st.code(ttl.read_text(encoding="utf-8")[:2500], language="turtle")
        st.caption("Vista previa limitada a 2500 caracteres para mantener legibilidad.")
    else:
        st.warning("Aún no se ha generado el grafo RDF.")

    if jsonld.exists():
        st.success("Archivo JSON-LD generado.")

    st.markdown("---")
    st.subheader("Validación SHACL")

    if ttl.exists():
        validator = ValidadorSHACL(ttl)
        resultado_validacion = validator.validar()

        col_v1, col_v2 = st.columns(2)

        with col_v1:
            card(
                "Noticias validadas",
                resultado_validacion["noticias_validadas"],
                "Recursos tipo simanw:Noticia"
            )

        with col_v2:
            card(
                "Violaciones",
                resultado_validacion["total_violaciones"],
                "Errores estructurales detectados"
            )

        if resultado_validacion["total_violaciones"] == 0:
            st.success("Validación completada sin violaciones estructurales.")
        else:
            st.warning("Se encontraron violaciones estructurales en el grafo.")

            tabla_html(pd.DataFrame(resultado_validacion["violaciones"]))

    st.markdown("---")
    st.subheader("Consultas SPARQL externas documentadas")

    consultas_ext = consultas_documentadas()

    opcion_endpoint = st.selectbox(
        "Endpoint",
        list(consultas_ext.keys())
    )

    consulta_info = consultas_ext[opcion_endpoint]

    st.write(f"Endpoint: `{consulta_info['endpoint']}`")
    st.write(consulta_info["descripcion"])
    st.code(consulta_info["query"], language="sparql")

    if opcion_endpoint == "wikidata":
        if st.button("Ejecutar consulta Wikidata"):
            with st.spinner("Consultando Wikidata..."):
                resultado = ejecutar_consulta_wikidata()

            if resultado["ok"]:
                st.success("Consulta ejecutada correctamente.")
                if resultado["resultados"]:
                    tabla_html(pd.DataFrame(resultado["resultados"]))
                else:
                    st.info("La consulta no devolvió resultados.")
            else:
                st.warning(
                    "No fue posible ejecutar la consulta externa. "
                    "Puede deberse a falta de internet, bloqueo del endpoint o dependencia faltante."
                )
                st.code(resultado["error"])

elif seccion == "Análisis de hilo":
    st.title("Análisis de hilo de discusión")

    analizador = AnalizadorHiloDiscusion()
    mensajes = hilo_demo()
    analizador.cargar_hilo(mensajes)

    resumen = analizador.resumen_hilo()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card("Mensajes", resumen["total_mensajes"], "Total del hilo")
    with col2:
        card("Participantes", resumen["participantes"], "Usuarios únicos")
    with col3:
        card("Tono", resumen["tono"], "Tono general")
    with col4:
        card("Promedio", f"{resumen['sentimiento_promedio']:+.2f}", "Sentimiento")

    st.subheader("Mensajes del hilo")

    tabla_html(pd.DataFrame(mensajes))

    st.subheader("Evolución del sentimiento")

    evolucion = analizador.evolucion_sentimiento()

    df_evo = pd.DataFrame(evolucion)

    fig = px.line(
        df_evo,
        x="posicion",
        y="tendencia",
        markers=True
    )

    fig.update_layout(
        paper_bgcolor="#F7F1E8",
        plot_bgcolor="#F7F1E8",
        font_color="#2B211E",
        xaxis_title="Mensaje",
        yaxis_title="Tendencia de sentimiento"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Subtemas detectados")

    subtemas = analizador.detectar_subtemas()

    filas_subtemas = []

    for cluster_id, info in subtemas.items():
        filas_subtemas.append({
            "Subtema": f"Subtema {cluster_id + 1}",
            "Mensajes": info["n_mensajes"],
            "Palabras clave": ", ".join(info["keywords"])
        })

    tabla_html(pd.DataFrame(filas_subtemas))

    st.subheader("Usuarios más activos")

    tabla_html(pd.DataFrame([
        {"Usuario": usuario, "Mensajes": total}
        for usuario, total in resumen["usuarios_activos"]
    ]))

elif seccion == "Reportes":
    st.title("Reportes automáticos")

    reporte = Path("outputs/reports/reporte_final_simanw.txt")
    manifiesto = Path("outputs/reports/manifiesto_ejecucion.json")

    if reporte.exists():
        st.subheader("Reporte final")
        st.text_area("Contenido", reporte.read_text(encoding="utf-8"), height=400)
    else:
        st.warning("Aún no existe reporte final.")

    if manifiesto.exists():
        st.subheader("Manifiesto de ejecución")
        st.json(json.loads(manifiesto.read_text(encoding="utf-8")))

    reporte_clasificacion_path = Path("outputs/reports/reporte_clasificacion.json")

    if reporte_clasificacion_path.exists():
        st.subheader("Evaluación multimodelo de clasificación")

        reporte_clasificacion = json.loads(
            reporte_clasificacion_path.read_text(encoding="utf-8")
        )

        comparacion = reporte_clasificacion.get("comparacion_modelos", {})
        mejor = reporte_clasificacion.get("mejor_modelo_multimodelo", "No disponible")

        st.write(f"Modelo seleccionado automáticamente: **{mejor}**")

        filas = []

        for modelo, datos in comparacion.items():
            if "accuracy_mean" in datos:
                filas.append({
                    "Modelo": modelo,
                    "Accuracy": round(datos["accuracy_mean"], 4),
                    "Desviación": round(datos["accuracy_std"], 4)
                })
            else:
                filas.append({
                    "Modelo": modelo,
                    "Accuracy": "Error",
                    "Desviación": datos.get("error", "")[:40]
                })

        if filas:
            tabla_html(pd.DataFrame(filas))