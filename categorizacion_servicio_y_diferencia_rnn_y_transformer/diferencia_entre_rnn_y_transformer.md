# Diferencia entre RNN y un transformer, ventajas, limitaciones, que tipo de dataset arrojan y si es supervisado, no supervisado o semi supervisado

# RNN (REDES NEURONALES RECURRENTES)

- Flujo de Informacion -> Secuencial: cada salida depende de la entrada actual y del estado oculto previo.
- Manejo de dependencia a largo plazo -> Limitado, problemas de gradiente desvanecido/explosivo, incluso con variantes como LSTM o GRU.
- Posiciones en la secuencia -> Implícitas por la estructura recurrente.
- Velocidad de entrenamiento -> Más lenta debido al procesamiento secuencial.

**Ventajas**

- Simples y conceptualmente intuitivas para secuencias de datos.
- Útiles para datasets de secuencias de longitud moderada.
- Consumo computacional menor para secuencias cortas.

**Limitaciones**

- Difíciles de entrenar para secuencias muy largas.
- Poca escalabilidad para grandes datasets.
- Suelen ser lentas en inferencia y entrenamiento debido al procesamiento secuencial.

**Tipo de Dataset**

- Secuencias temporales de tamaño moderado

**Ejemplos**

- Series de tiempo, texto de longitud limitada, predicción de señales biológicas

# TRANSFORMER

- Flujo de Informacion -> Paralelo: usa mecanismo de self-attention para procesar todas las posiciones de la secuencia simultáneamente.
- Manejo de dependencia a largo plazo -> Eficiente: la atención puede relacionar cualquier par de posiciones independientemente de la distancia, capturando dependencias a largo plazo de manera directa.
- Posiciones en la secuencia -> Explícitas mediante embeddings posicionales.
- Velocidad de entrenamiento -> Rápido en entrenamiento por procesamiento paralelo; entrenamiento más escalable para grandes datasets.

**Ventajas**

- Captura relaciones complejas y dependencias largas eficientemente.
- Entrenamiento altamente paralelizable, adaptándose mejor a grandes datasets.
- Ha demostrado superioridad en tareas de NLP (traducción, resumen), visión (ViT), y multimodalidad.

**Limitaciones**

- Mayor consumo de memoria, especialmente en secuencias muy largas.
- Necesitan grandes cantidades de datos para rendimiento óptimo.
- Modelos grandes y complejos pueden ser costosos en infraestructura y energía.

**Tipo de Dataset**

- Cualquier secuencia, grandes corpus

**Ejemplos**

- Traducción automática, resumen de texto, clasificación de documentos, audio, visión computacional, multimodalidad

# Comparacion

- Naturaleza secuencial: Ambos operan sobre secuencias de datos y pueden modelar dependencias entre elementos.
- Representación aprendida: Ambos producen representaciones vectoriales que reflejan contexto.
- Diferencia clave: El RNN depende de propagación recurrente, mientras que el Transformer depende de la atención global y procesamiento paralelo.