# Algoritmos de Aprendizaje Supervisado, No Supervisado y Semi Supervisado

## Supervisado

**Usan datos etiquetados: sabes la respuesta correcta durante el entrenamiento**

**Algoritmos Generales**
- Regresión Lineal: Predice valores continuos (ej: precios, temperatura).
- Regresión Logística: Clasificación binaria (ej: spam / no spam).
- Máquinas de Soporte Vectorial (SVM): Clasificación y regresión separando datos con hiperplanos.
- Árboles de Decisión: Modelo basado en reglas tipo “si-entonces”.
- K-Nearest Neighbors (KNN): Clasifica según los vecinos más cercanos.

**Supervisado: sabes la respuesta → aprendes a predecirla.**

**Algoritmos para Clasificacion de Texto**

**Naive Bayes (Multinomial)**
- Muy usado en NLP clásico (spam, sentimientos).
- Funciona bien con bolsas de palabras (Bag of Words, TF-IDF).

**Máquinas de Soporte Vectorial (SVM)**
- Muy efectivo en clasificación de textos con alta dimensionalidad.

**Regresión Logística**
- Simple pero muy competitiva en problemas de texto.

**Árboles de Decisión / Random Forest**
- Menos comunes en texto, pero aplicables.

**Redes Neuronales (LSTM / Transformers)**
- Ejemplo: modelos tipo BERT
- Estado del arte en NLP moderno.

***TIPOS***

**Clasificación**
- Predicen categorías (ej: correo spam o no spam).
- Ej: SVM, KNN, árboles de decisión.

**Regresión**
- Predicen valores numéricos continuos (ej: precio de una casa).
- Ej: regresión lineal.

**Ensamblado (Ensemble Learning)**
- Combinan varios modelos para mejorar precisión.
- Ej: Random Forest, Gradient Boosting.

**Aprendizaje basado en instancias**
- No generaliza mucho, usa los datos directamente.
- Ej: KNN.

**Aprendizaje basado en modelos (paramétricos)**
- Ajustan parámetros a partir de los datos.
- Ej: regresión logística, redes neuronales.

**En supervisado, los tipos dependen del tipo de salida (clasificar, predecir, combinar modelos).**

## No Supervisado

**No hay etiquetas; el modelo descubre patrones**

**Algoritmos Generales**
- K-Means: Agrupa datos en clusters según similitud.
- Clustering Jerárquico: Construye grupos en forma de árbol (dendrograma).
- DBSCAN: Detecta clusters basados en densidad.
- Análisis de Componentes Principales (PCA): Reduce dimensionalidad manteniendo información relevante.
- Mapas Autoorganizados (SOM): Red neuronal que agrupa datos en un mapa.

**No supervisado: no sabes la respuesta → encuentras patrones ocultos.**

**Algoritmos para Clasificacion de Texto**

**Aquí realmente es agrupamiento, no clasificación directa**

**K-Means**
- Agrupa documentos por similitud.

**Clustering Jerárquico**
- Forma árboles de similitud entre textos.

**Latent Dirichlet Allocation (LDA)**
- Modelo de temas (topic modeling).

**Non-negative Matrix Factorization (NMF)**
- Extrae temas latentes.

**DBSCAN**
- Agrupa textos según densidad.

**Aquí no hay etiquetas reales, se interpretan los grupos.**

***TIPOS***

**Clustering (agrupamiento)**
- Agrupan datos similares.
- Ej: K-Means, DBSCAN.

**Reducción de dimensionalidad**
- Simplifican datos manteniendo información clave.
- Ej: PCA.

**Reglas de asociación**
- Encuentran relaciones entre variables.
- Ej: análisis de canasta de mercado (Apriori).

**Detección de anomalías**
- Identifican datos fuera de lo normal.
- Ej: Isolation Forest.

**Modelos generativos**
- Aprenden la distribución de los datos para generar nuevos ejemplos.
- Ej: Gaussian Mixture Models.

**En no supervisado, dependen del tipo de patrón que quieres descubrir (grupos, relaciones, estructura).**

## Semi Supervisado

**Combina datos etiquetados (pocos) y no etiquetados (muchos), así que los algoritmos suelen ser extensiones de los supervisados o técnicas específicas.**

**Algoritmos Generales**
- Self-Training (Autoentrenamiento): Entrenas un modelo con los datos etiquetados, luego el modelo predice etiquetas para datos no etiquetados y se agregan las predicciones más confiables al entrenamiento.
- Co-Training: Usa dos modelos diferentes (o dos vistas de los datos), cada modelo etiqueta datos para el otro y se apoyan mutuamente para mejorar.
- Label Propagation: Construye un grafo de datos y las etiquetas se “propagan” a puntos cercanos.
- Label Spreading: Variante de Label Propagation y es más robusto al ruido porque suaviza las etiquetas.
- Semi-Supervised SVM (S3VM): Extiende las Máquinas de Soporte Vectorial y usa datos no etiquetados para encontrar mejores fronteras de decisión.

**Todos estos métodos buscan aprovechar la idea de que: “los datos cercanos o similares probablemente pertenecen a la misma clase”**

**Algoritmos para Clasificacion de Texto**

**Self-Training con clasificadores (ej: SVM o Naive Bayes)**
- Usa pseudo-etiquetas en textos no etiquetados.

**Co-Training**
- Ej: usar texto + metadata (título/contenido) como dos vistas.

**Label Propagation**
- Propaga etiquetas entre textos similares (usando embeddings).

**Label Spreading**
- Variante más robusta al ruido.

**Pseudo-Labeling con redes neuronales**
- Muy usado con modelos tipo BERT o GPT-like.
