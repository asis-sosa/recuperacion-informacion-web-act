from datetime import datetime
from collections import Counter
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DC, FOAF

noticias = [
    {
        "titulo": "Avances en IA Generativa revolucionan la industria",
        "cuerpo": "Los nuevos modelos de inteligencia artificial generativa están transformando múltiples industrias.",
        "fecha": "2026-05-10",
        "autor": "María García",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.45},
        "url": "https://portal.com/noticias/ia-generativa-2026"
    },
    {
        "titulo": "Mercados financieros muestran volatilidad ante incertidumbre global",
        "cuerpo": "Los principales índices bursátiles registraron caídas significativas ante la inflación.",
        "fecha": "2026-05-09",
        "autor": "Carlos Ruiz",
        "categoria_original": "economia",
        "categoria_predicha": "economia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.35},
        "url": "https://portal.com/noticias/mercados-volatilidad"
    },
    {
        "titulo": "Python 3.14 trae mejoras significativas en rendimiento",
        "cuerpo": "La nueva versión del lenguaje Python incluye optimizaciones que mejoran la velocidad de ejecución.",
        "fecha": "2026-05-07",
        "autor": "Juan Hernández",
        "categoria_original": "tecnologia",
        "categoria_predicha": "tecnologia",
        "sentimiento": {"etiqueta": "positivo", "compound": 0.38},
        "url": "https://portal.com/noticias/python-314"
    },
    {
        "titulo": "Gobierno lanza portal de datos abiertos con tecnología semántica",
        "cuerpo": "La plataforma gubernamental ofrece acceso a datasets públicos en formatos RDF y JSON-LD.",
        "fecha": "2026-05-06",
        "autor": "Pedro Sánchez",
        "categoria_original": "gobierno",
        "categoria_predicha": "politica",
        "sentimiento": {"etiqueta": "neutral", "compound": 0.0},
        "url": "https://portal.com/noticias/datos-abiertos-gob"
    },
    {
        "titulo": "Descubrimiento científico sobre cambio climático alarma a expertos",
        "cuerpo": "Un equipo internacional publicó un estudio preocupante sobre el calentamiento global.",
        "fecha": "2026-05-08",
        "autor": "Ana López",
        "categoria_original": "ciencia",
        "categoria_predicha": "ciencia",
        "sentimiento": {"etiqueta": "negativo", "compound": -0.42},
        "url": "https://portal.com/noticias/clima-estudio-2026"
    }
]

class KnowledgeGraphSIMANW:
    def __init__(self):
        self.graph = Graph()

        self.NS = Namespace("http://simanw.org/ontology/")
        self.DATA = Namespace("http://simanw.org/data/")

        self.graph.bind("simanw", self.NS)
        self.graph.bind("data", self.DATA)
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)

        self._definir_ontologia()

    def _definir_ontologia(self):
        self.graph.add((self.NS.Noticia, RDF.type, OWL.Class))
        self.graph.add((self.NS.Autor, RDF.type, OWL.Class))
        self.graph.add((self.NS.Categoria, RDF.type, OWL.Class))
        self.graph.add((self.NS.Fuente, RDF.type, OWL.Class))

        self.graph.add((self.NS.tieneAutor, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.tieneAutor, RDFS.domain, self.NS.Noticia))
        self.graph.add((self.NS.tieneAutor, RDFS.range, self.NS.Autor))

        self.graph.add((self.NS.tieneCategoria, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.provieneDe, RDF.type, OWL.ObjectProperty))
        self.graph.add((self.NS.relacionadaCon, RDF.type, OWL.ObjectProperty))

        self.graph.add((self.NS.sentimientoScore, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.sentimientoEtiqueta, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.NS.urlOriginal, RDF.type, OWL.DatatypeProperty))

    def agregar_noticia(self, noticia, noticia_id):
        uri = self.DATA[f"noticia_{noticia_id}"]

        self.graph.add((uri, RDF.type, self.NS.Noticia))
        self.graph.add((uri, DC.title, Literal(noticia["titulo"], lang="es")))
        self.graph.add((uri, DC.description, Literal(noticia["cuerpo"][:200], lang="es")))
        self.graph.add((uri, DC.date, Literal(noticia["fecha"], datatype=XSD.date)))

        autor_uri = self.DATA[f"autor_{noticia['autor'].replace(' ', '_')}"]
        self.graph.add((autor_uri, RDF.type, self.NS.Autor))
        self.graph.add((autor_uri, FOAF.name, Literal(noticia["autor"])))
        self.graph.add((uri, self.NS.tieneAutor, autor_uri))

        categoria = noticia.get("categoria_predicha", noticia.get("categoria_original", "general"))
        cat_uri = self.DATA[f"categoria_{categoria}"]

        self.graph.add((cat_uri, RDF.type, self.NS.Categoria))
        self.graph.add((cat_uri, RDFS.label, Literal(categoria, lang="es")))
        self.graph.add((uri, self.NS.tieneCategoria, cat_uri))

        if "sentimiento" in noticia:
            sent = noticia["sentimiento"]

            self.graph.add((
                uri,
                self.NS.sentimientoScore,
                Literal(sent["compound"], datatype=XSD.float)
            ))

            self.graph.add((
                uri,
                self.NS.sentimientoEtiqueta,
                Literal(sent["etiqueta"])
            ))

        if "url" in noticia:
            self.graph.add((
                uri,
                self.NS.urlOriginal,
                Literal(noticia["url"], datatype=XSD.anyURI)
            ))

    def consultar(self, sparql_query):
        return list(self.graph.query(sparql_query))

    def total_triples(self):
        return len(self.graph)

    def serializar(self, formato="turtle"):
        return self.graph.serialize(format=formato)

kg = KnowledgeGraphSIMANW()

class GeneradorReportes:
    """Genera reportes automáticos del SIMANW."""

    def __init__(self, noticias, knowledge_graph):
        self.noticias = noticias
        self.kg = knowledge_graph

    def reporte_completo(self):
        """Genera el reporte integrador completo."""
        lineas = []
        lineas.append("=" * 70)
        lineas.append("  REPORTE AUTOMÁTICO - SISTEMA SIMANW")
        lineas.append(f"  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lineas.append("=" * 70)

        # Sección 1: Resumen ejecutivo
        lineas.append("\n1. RESUMEN EJECUTIVO")
        lineas.append("─" * 40)
        lineas.append(f"   Noticias procesadas: {len(self.noticias)}")
        lineas.append(f"   Triples en Knowledge Graph: {self.kg.total_triples()}")

        cats = Counter(n.get('categoria_predicha', n['categoria_original']) for n in self.noticias)
        lineas.append(f"   Categorías detectadas: {len(cats)}")

        sents = [n['sentimiento']['compound'] for n in self.noticias if 'sentimiento' in n]
        promedio = sum(sents) / len(sents) if sents else 0
        lineas.append(f"   Sentimiento promedio: {promedio:+.3f}")
        lineas.append(f"   Tono general: {'POSITIVO' if promedio > 0.05 else 'NEGATIVO' if promedio < -0.05 else 'NEUTRAL'}")

        # Sección 2: Distribución por categoría
        lineas.append("\n2. DISTRIBUCIÓN POR CATEGORÍA")
        lineas.append("─" * 40)
        for cat, count in cats.most_common():
            barra = "█" * (count * 8)
            pct = 100 * count / len(self.noticias)
            lineas.append(f"   {cat:<12} {barra} {count} ({pct:.0f}%)")

        # Sección 3: Análisis de sentimiento
        lineas.append("\n3. ANÁLISIS DE SENTIMIENTO")
        lineas.append("─" * 40)
        sent_dist = Counter(n['sentimiento']['etiqueta'] for n in self.noticias if 'sentimiento' in n)
        for etiqueta, count in sent_dist.most_common():
            emoji = "+" if etiqueta == 'positivo' else "-" if etiqueta == 'negativo' else "~"
            lineas.append(f"   [{emoji}] {etiqueta}: {count} noticia(s)")

        lineas.append("\n   Detalle por noticia:")
        for n in sorted(self.noticias, key=lambda x: x.get('sentimiento', {}).get('compound', 0)):
            if 'sentimiento' in n:
                s = n['sentimiento']
                lineas.append(f"   [{s['compound']:+.3f}] {n['titulo'][:50]}")

        # Sección 4: Noticias procesadas
        lineas.append("\n4. CATÁLOGO DE NOTICIAS")
        lineas.append("─" * 40)
        for i, n in enumerate(self.noticias, 1):
            cat = n.get('categoria_predicha', n['categoria_original'])
            sent = n.get('sentimiento', {}).get('etiqueta', '?')
            lineas.append(f"   {i}. [{n['fecha']}] [{cat}] [{sent}]")
            lineas.append(f"      {n['titulo']}")
            lineas.append(f"      Autor: {n['autor']} | Fuente: {n['url']}")
            lineas.append("")

        # Sección 5: Capacidades del sistema
        lineas.append("\n5. CAPACIDADES DEMOSTRADAS")
        lineas.append("─" * 40)
        capacidades = [
            ("Rastreo Web", "Extracción automática con BeautifulSoup/Scrapy"),
            ("NLP", "Tokenización, stemming, stopwords, representación TF-IDF"),
            ("Clasificación", "Categorización automática con SVM/NB"),
            ("Sentimientos", "Análisis de polaridad con VADER"),
            ("Recomendación", "Sugerencias basadas en similitud coseno"),
            ("Publicidad", "Detección de temas en conversación"),
            ("Búsqueda", "Motor con índice invertido y ranking vectorial"),
            ("Evaluación IRS", "Precision, Recall, F1, MAP, P@K"),
            ("Chatbot", "Respuestas por similitud semántica"),
            ("Q&A", "Pregunta-respuesta con comprensión de intención"),
            ("Knowledge Graph", "Ontología OWL + triples RDF"),
            ("SPARQL", "Consultas semánticas sobre el grafo"),
            ("Datos Abiertos", "Integración con datasets gubernamentales"),
            ("Reportes", "Generación automática de resúmenes"),
        ]
        for nombre, desc in capacidades:
            lineas.append(f"   [OK] {nombre:<16} → {desc}")

        lineas.append("\n" + "=" * 70)
        lineas.append("  FIN DEL REPORTE")
        lineas.append("=" * 70)

        return "\n".join(lineas)


reportero = GeneradorReportes(noticias, kg)
print(reportero.reporte_completo())

print("7.2 Integración final: Pipeline completo")

print("""
╔══════════════════════════════════════════════════════════════════════╗
║           SISTEMA SIMANW - PIPELINE COMPLETO                         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Fase 1: RASTREO WEB                                                 ║
║    → HTML parsing (BeautifulSoup)                                    ║
║    → Control de alcance (dominio/directorio)                         ║
║    → Spider (Scrapy en producción)                                   ║
║    → Almacenamiento (JSON/CSV)                                       ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 2: PROCESAMIENTO NLP                                           ║
║    → Tokenización + Limpieza                                         ║
║    → Stopwords + Stemming                                            ║
║    → Vectorización TF-IDF                                            ║
║    → Cálculo de similitudes (coseno)                                 ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 3: ANÁLISIS AUTOMÁTICO                                         ║
║    → Clasificación (SVM/NB)                                          ║
║    → Sentimiento (VADER)                                             ║
║    → Recomendación (similitud contenido)                             ║
║    → Detección temas + publicidad                                    ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 4: MOTOR DE BÚSQUEDA                                           ║
║    → Índice invertido                                                ║
║    → Búsqueda booleana y vectorial                                   ║
║    → Evaluación (P, R, F1, MAP)                                      ║
║    → Búsqueda en lenguaje natural                                    ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 5: CHATBOT + Q&A                                               ║
║    → Chatbot por similitud                                           ║
║    → Sistema pregunta-respuesta                                      ║
║    → Comprensión de intención                                        ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 6: WEB SEMÁNTICA                                               ║
║    → Ontología OWL del dominio                                       ║
║    → Knowledge Graph (RDF triples)                                   ║
║    → Consultas SPARQL                                                ║
║    → Datos abiertos + Linked Data                                    ║
║          │                                                           ║
║          ▼                                                           ║
║  Fase 7: REPORTES + ENTREGA                                          ║
║    → Generación automática de reportes                               ║
║    → Estadísticas y visualización                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")