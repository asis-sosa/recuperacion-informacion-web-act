from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score


class ClasificadorNoticias:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.clasificador = LinearSVC(max_iter=3000)
        self.entrenado = False
        self.categorias = []

    def datos_entrenamiento_base(self):
        textos = [
            "inteligencia artificial machine learning algoritmos redes neuronales deep learning",
            "nuevo procesador computadora software desarrollo programación tecnología",
            "startup tecnológica lanza aplicación innovadora plataforma digital",
            "robot automatización industria software empresa tecnología",

            "mercados financieros bolsa acciones inversión capital rendimiento",
            "inflación economía banco central tasas interés política monetaria",
            "desempleo crisis económica recesión PIB crecimiento producto interno",
            "comercio internacional exportaciones importaciones aranceles tratado",

            "estudio científico investigadores descubrimiento laboratorio publicación",
            "cambio climático calentamiento global temperatura emisiones carbono",
            "vacuna tratamiento médico salud enfermedad hospital pacientes",
            "espacio NASA cohete satélite misión exploración astronauta",

            "elecciones candidato presidente congreso voto democracia partido",
            "gobierno ley reforma política pública decreto legislación",
            "seguridad pública policía crimen delito justicia tribunal",
            "presupuesto gasto público programa social gobierno federal",

            "hospital médico cirugía tratamiento pacientes salud",
            "vacuna enfermedad prevención medicina clínica salud",
            "investigación médica diagnóstico especialistas hospital",

            "videojuego consola playstation xbox nintendo",
            "videojuego lanzamiento gaming jugador competitivo",
            "esports torneo videojuego multiplayer estrategia",
        ]

        etiquetas = [
            "tecnologia", "tecnologia", "tecnologia", "tecnologia",
            "economia", "economia", "economia", "economia",
            "ciencia", "ciencia", "ciencia", "ciencia",
            "politica", "politica", "politica", "politica",
            "salud", "salud", "salud",
            "videojuegos", "videojuegos", "videojuegos",
        ]

        return textos, etiquetas

    def entrenar(self):
        textos, etiquetas = self.datos_entrenamiento_base()

        X = self.vectorizer.fit_transform(textos)
        self.clasificador.fit(X, etiquetas)

        self.categorias = sorted(list(set(etiquetas)))
        self.entrenado = True

        scores = cross_val_score(
            self.clasificador,
            X,
            etiquetas,
            cv=3
        )

        return {
            "muestras_entrenamiento": len(textos),
            "categorias": self.categorias,
            "accuracy_cv": float(scores.mean())
        }

    def predecir(self, texto):
        if not self.entrenado:
            self.entrenar()

        X = self.vectorizer.transform([texto])
        return self.clasificador.predict(X)[0]

    def clasificar_noticias(self, noticias):
        reporte = self.entrenar()
        clasificadas = []

        distribucion = {}

        for noticia in noticias:
            texto = f"{noticia['titulo']} {noticia['cuerpo']}"
            prediccion = self.predecir(texto)

            noticia_clasificada = noticia.copy()
            noticia_clasificada["categoria_predicha"] = prediccion

            distribucion[prediccion] = distribucion.get(prediccion, 0) + 1
            clasificadas.append(noticia_clasificada)

        reporte["distribucion_predicha"] = distribucion
        reporte["total_clasificadas"] = len(clasificadas)

        return clasificadas, reporte