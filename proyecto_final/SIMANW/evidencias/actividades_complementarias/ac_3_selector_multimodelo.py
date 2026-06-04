from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import numpy as np

class SelectorModelo:
    """
    AC-3: Entrena múltiples modelos y selecciona el mejor automáticamente.
    El alumno debe agregar más datos de entrenamiento de sus noticias reales.
    """

    def __init__(self):
        self.modelos = {
            'Naive Bayes': MultinomialNB(alpha=0.1),
            'SVM Lineal': LinearSVC(max_iter=3000, C=1.0),
            'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        }
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.mejor_modelo = None
        self.resultados = {}

    def evaluar_todos(self, textos, etiquetas, cv_folds=3):
        """Evalúa todos los modelos con validación cruzada."""
        X = self.vectorizer.fit_transform(textos)
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

        for nombre, modelo in self.modelos.items():
            try:
                scores = cross_val_score(modelo, X, etiquetas, cv=cv, scoring='accuracy')
                self.resultados[nombre] = {
                    'accuracy_mean': scores.mean(),
                    'accuracy_std': scores.std(),
                    'scores': scores.tolist()
                }
            except Exception as e:
                self.resultados[nombre] = {'error': str(e)}

        # Seleccionar el mejor
        validos = {k: v for k, v in self.resultados.items() if 'accuracy_mean' in v}
        if validos:
            mejor_nombre = max(validos, key=lambda k: validos[k]['accuracy_mean'])
            self.mejor_modelo = (mejor_nombre, self.modelos[mejor_nombre])
            # Entrenar el mejor con todos los datos
            self.mejor_modelo[1].fit(X, etiquetas)

        return self.resultados

    def predecir(self, textos):
        """Predice usando el mejor modelo seleccionado."""
        if not self.mejor_modelo:
            raise ValueError("Primero ejecuta evaluar_todos()")
        X = self.vectorizer.transform(textos)
        return self.mejor_modelo[1].predict(X)

    def reporte(self):
        """Genera reporte comparativo de modelos."""
        lineas = ["Modelo                  | Accuracy   | Std Dev"]
        lineas.append("-" * 50)
        for nombre, res in sorted(self.resultados.items(),
                                  key=lambda x: x[1].get('accuracy_mean', 0),
                                  reverse=True):
            if 'accuracy_mean' in res:
                marca = " ★" if self.mejor_modelo and nombre == self.mejor_modelo[0] else ""
                lineas.append(f"{nombre:<23} | {res['accuracy_mean']:.4f}     | {res['accuracy_std']:.4f}{marca}")
            else:
                lineas.append(f"{nombre:<23} | ERROR      | {res.get('error', '')[:20]}")
        return "\n".join(lineas)


# Datos expandidos para demostración
textos_ac3 = [
    "inteligencia artificial deep learning redes neuronales transformers",
    "programación software desarrollo aplicaciones web python javascript",
    "startup tecnológica innovación digital plataforma cloud",
    "ciberseguridad hackers vulnerabilidad protección datos privacidad",
    "inflación tasas interés banco central política monetaria",
    "bolsa acciones mercado valores inversión rendimiento portafolio",
    "desempleo recesión económica crisis laboral empleo informal",
    "comercio exportaciones importaciones balanza aranceles tratado",
    "investigación científica laboratorio experimento publicación revista",
    "cambio climático emisiones carbono calentamiento temperatura global",
    "vacuna medicamento ensayo clínico pacientes tratamiento hospital",
    "espacio cohete satélite misión astronauta exploración lunar",
    "elecciones presidente candidato partido campaña votación democracia",
    "congreso legisladores reforma ley aprobación dictamen senado",
    "seguridad policía crimen organizado justicia tribunal sentencia",
    "gobierno programa social presupuesto política pública decreto",
]
etiquetas_ac3 = [
    'tecnologia', 'tecnologia', 'tecnologia', 'tecnologia',
    'economia', 'economia', 'economia', 'economia',
    'ciencia', 'ciencia', 'ciencia', 'ciencia',
    'politica', 'politica', 'politica', 'politica',
]

selector = SelectorModelo()
resultados = selector.evaluar_todos(textos_ac3, etiquetas_ac3, cv_folds=3)

print("=== AC-3: Selección Automática de Modelo ===\n")
print(selector.reporte())
print(f"\nModelo seleccionado: {selector.mejor_modelo[0]}")

# Probar con nuevos textos
nuevos = [
    "nueva aplicación de machine learning para detectar fraudes",
    "el presidente anunció reformas al sistema de justicia",
    "los mercados cerraron con pérdidas por tercer día consecutivo",
]
predicciones = selector.predecir(nuevos)
print(f"\nPredicciones con el mejor modelo:")
for texto, pred in zip(nuevos, predicciones):
    print(f"  [{pred}] {texto[:50]}...")