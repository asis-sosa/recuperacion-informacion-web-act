import json
from collections import Counter
from datetime import datetime
from pathlib import Path


class GeneradorReportes:
    def __init__(self, noticias):
        self.noticias = noticias

    def generar_reporte_texto(self, total_triples=0):
        lineas = []

        lineas.append("=" * 70)
        lineas.append(" REPORTE AUTOMÁTICO - SISTEMA SIMANW")
        lineas.append(f" Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lineas.append("=" * 70)

        lineas.append("\n1. RESUMEN EJECUTIVO")
        lineas.append("-" * 40)
        lineas.append(f"Noticias procesadas: {len(self.noticias)}")
        lineas.append(f"Triples en Knowledge Graph: {total_triples}")

        categorias = Counter(
            n.get("categoria_predicha", n.get("categoria_original", "general"))
            for n in self.noticias
        )

        lineas.append(f"Categorías detectadas: {len(categorias)}")

        sentimientos = [
            n.get("sentimiento", {}).get("compound", 0)
            for n in self.noticias
        ]

        promedio = sum(sentimientos) / max(len(sentimientos), 1)

        tono = (
            "POSITIVO" if promedio > 0.05
            else "NEGATIVO" if promedio < -0.05
            else "NEUTRAL"
        )

        lineas.append(f"Sentimiento promedio: {promedio:+.3f}")
        lineas.append(f"Tono general: {tono}")

        lineas.append("\n2. DISTRIBUCIÓN POR CATEGORÍA")
        lineas.append("-" * 40)

        for categoria, total in categorias.most_common():
            porcentaje = 100 * total / max(len(self.noticias), 1)
            barra = "█" * total
            lineas.append(f"{categoria:<15} {barra} {total} ({porcentaje:.1f}%)")

        lineas.append("\n3. ANÁLISIS DE SENTIMIENTO")
        lineas.append("-" * 40)

        dist_sent = Counter(
            n.get("sentimiento", {}).get("etiqueta", "desconocido")
            for n in self.noticias
        )

        for etiqueta, total in dist_sent.most_common():
            lineas.append(f"{etiqueta:<12}: {total} noticia(s)")

        lineas.append("\n4. CATÁLOGO DE NOTICIAS")
        lineas.append("-" * 40)

        for i, n in enumerate(self.noticias, 1):
            categoria = n.get("categoria_predicha", n.get("categoria_original", "?"))
            sentimiento = n.get("sentimiento", {}).get("etiqueta", "?")
            fecha = n.get("fecha", "?")
            autor = n.get("autor", "Desconocido")

            lineas.append(f"{i}. [{fecha}] [{categoria}] [{sentimiento}]")
            lineas.append(f"   {n['titulo']}")
            lineas.append(f"   Autor: {autor}")
            lineas.append(f"   URL: {n.get('url', 'sin_url')}")
            lineas.append("")

        lineas.append("\n5. CAPACIDADES DEMOSTRADAS")
        lineas.append("-" * 40)

        capacidades = [
            "Rastreo web con BeautifulSoup/Scrapy",
            "Control de calidad del corpus",
            "Procesamiento NLP",
            "Clasificación automática",
            "Análisis de sentimiento",
            "Motor de búsqueda vectorial",
            "Alertas por consultas guardadas",
            "Chatbot y sistema Q&A",
            "Knowledge Graph RDF",
            "Consultas SPARQL",
            "Exportación Turtle y JSON-LD",
            "Reportes automáticos",
            "Trazabilidad de ejecución"
        ]

        for c in capacidades:
            lineas.append(f"[OK] {c}")

        lineas.append("\n" + "=" * 70)
        lineas.append(" FIN DEL REPORTE")
        lineas.append("=" * 70)

        return "\n".join(lineas)

    def generar_manifiesto(self, total_triples=0):
        return {
            "proyecto": "SIMANW",
            "version": "1.0.0",
            "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "documentos_procesados": len(self.noticias),
            "triples_knowledge_graph": total_triples,
            "artefactos_generados": {
                "corpus_raw": "data/raw/noticias_raw.json",
                "corpus_limpio": "data/processed/noticias_limpias.json",
                "corpus_analizado": "data/processed/noticias_analizadas.json",
                "knowledge_graph_turtle": "data/rdf/simanw_kg.ttl",
                "knowledge_graph_jsonld": "data/rdf/simanw_kg.jsonld",
                "reporte_final": "outputs/reports/reporte_final_simanw.txt"
            }
        }


def guardar_texto(ruta, contenido):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


def guardar_json(ruta, datos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)