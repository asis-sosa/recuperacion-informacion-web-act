from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold


class SelectorModelo:
    def __init__(self):
        self.modelos = {
            "Naive Bayes": MultinomialNB(alpha=0.1),
            "SVM Lineal": LinearSVC(max_iter=3000, C=1.0),
            "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0),
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        }

        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.mejor_modelo = None
        self.resultados = {}

    def evaluar_todos(self, textos, etiquetas, cv_folds=3):
        X = self.vectorizer.fit_transform(textos)
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

        for nombre, modelo in self.modelos.items():
            try:
                scores = cross_val_score(
                    modelo,
                    X,
                    etiquetas,
                    cv=cv,
                    scoring="accuracy"
                )

                self.resultados[nombre] = {
                    "accuracy_mean": float(scores.mean()),
                    "accuracy_std": float(scores.std()),
                    "scores": scores.tolist()
                }

            except Exception as e:
                self.resultados[nombre] = {
                    "error": str(e)
                }

        validos = {
            k: v for k, v in self.resultados.items()
            if "accuracy_mean" in v
        }

        if validos:
            mejor_nombre = max(
                validos,
                key=lambda k: validos[k]["accuracy_mean"]
            )

            self.mejor_modelo = (
                mejor_nombre,
                self.modelos[mejor_nombre]
            )

            self.mejor_modelo[1].fit(X, etiquetas)

        return self.resultados

    def obtener_mejor_modelo(self):
        if not self.mejor_modelo:
            return None

        return self.mejor_modelo[0]