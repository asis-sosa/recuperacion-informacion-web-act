# Actividad: Reducción de Dimensionalidad en Recuperación de Información

## Objetivo

**Comparar la reducción de dimensionalidad realizada manualmente (“a ojo”) con métodos automáticos como TF-IDF + SVD, para entender sus ventajas y limitaciones.**

## Dataset (Documentos)

## Documento 1 – Tecnología

**El aprendizaje automático es una rama de la inteligencia artificial que permite a las computadoras aprender a partir de datos sin ser programadas explícitamente. Se utiliza en aplicaciones como reconocimiento de voz, visión por computadora y sistemas de recomendación.**

## Documento 2 – Salud

**La salud pública se enfoca en la prevención de enfermedades y la promoción del bienestar en la población. Incluye campañas de vacunación, educación sanitaria y el control de epidemias.**

## Documento 3 – Deportes

**El fútbol es uno de los deportes más populares en el mundo. Requiere habilidades físicas, trabajo en equipo y estrategias para anotar goles y ganar partidos.**

## Documento 4 – Tecnología

**Los sistemas de inteligencia artificial pueden analizar grandes volúmenes de datos para identificar patrones y tomar decisiones automatizadas en diversos contextos.**

## Documento 5 – Educación

**La educación moderna incorpora tecnologías digitales para mejorar el aprendizaje. Plataformas en línea, simuladores y recursos interactivos facilitan la enseñanza.**

## Documento 6 – Medio Ambiente

**El cambio climático afecta a los ecosistemas y provoca fenómenos extremos como sequías, inundaciones y aumento de temperatura global.**

## Documento 7 – Economía

**La inflación es el aumento generalizado de los precios de bienes y servicios en una economía durante un periodo de tiempo.**

## Documento 8 – Tecnología

**Las redes neuronales profundas permiten el desarrollo de sistemas avanzados de reconocimiento de imágenes y procesamiento de lenguaje natural.**

## Documento 9 – Salud

**Una alimentación balanceada y el ejercicio regular son fundamentales para prevenir enfermedades y mantener una buena calidad de vida.**

## Documento 10 – Educación

**El aprendizaje en línea ha crecido significativamente gracias al acceso a internet y a plataformas digitales educativas.**

## Parte 1: Reducción “a ojo”

### Instrucciones

**Para cada documento:**
- Selecciona las palabras más importantes
- Reduce cada texto a máximo 5 palabras clave

### Entregable - Ejemplo

| Docuemnto | Palabras Clave|
|-----------|---------------|
| Doc 1 | ... |
| Doc 2 | ... |

### Entregable - Resultado

| Docuemnto | Palabras Clave|
|-----------|---------------|
| Doc 1 | aprendizaje automático inteligencia artificial aprender |
| Doc 2 | salud pública prevención enfermedades bienestar |
| Doc 3 | fútbol deportes populares mundo |
| Doc 4 | sistemas inteligencia artificial analizar datos |
| Doc 5 | educación moderna tecnologías digitales aprendizaje |
| Doc 6 | cambio climático afecta ecosistemas fenómenos |
| Doc 7 | inflación aumento generalizado precios economía |
| Doc 8 | redes neuronales desarrollo sistemas avanzados |
| Doc 9 | alimentación balanceada ejercicio prevenir enfermedades |
| Doc 10 | aprendizaje línea crecido acceso internet |

## Parte 2: Discusión

### Responde:
- ¿Qué criterio utilizaste para seleccionar palabras?
- ¿Coincidiste con otros compañeros?
- ¿Qué dificultades encontraste?

### Respuestas

- Intuicion, unicamente al comienzo de la frase tome las palabras con conceptos mas profundos a lo que se esperaba, dado la limitacion del objetivo, no tuve mucha oportunidad de escoger mas, pero con las seleccionadas es posible entender un poco hacia que tema se va dirigiendo.
- Desconozco si hubo quienes compartian mi misma conclusion, pero considero que habria algunos que considerarian mis opciones como validas.
- La mayor doficultad fue la limitacion, disminuir todo un tema a solo cinco palabras es bastante limitado, muy probablemente hubo contenido que me pude haber brincado por solo tener que contar con solo 5 palabras en cada tema.

## Parte 3: Representación con TF-IDF

from sklearn.feature_extraction.text import TfidfVectorizer

documentos = [
"El aprendizaje automático es una rama de la inteligencia artificial...",
"La salud pública se enfoca en la prevención de enfermedades...",
"El fútbol es uno de los deportes más populares...",
"Los sistemas de inteligencia artificial pueden analizar grandes datos...",
"La educación moderna incorpora tecnologías digitales...",
"El cambio climático afecta a los ecosistemas...",
"La inflación es el aumento de precios...",
"Las redes neuronales profundas permiten...",
"Una alimentación balanceada y el ejercicio...",
"El aprendizaje en línea ha crecido..."
]

vectorizer = TfidfVectorizer(stop_words='spanish')
X = vectorizer.fit_transform(documentos)

print(X.shape)

### Resultados

- Debido a que la linea -> "vectorizer = TfidfVectorizer(stop_words='spanish')", marca un error, se tuvo que utilizar un codigo mejorado ("representacion_tfidf_vm.py") que integra el uso de nltk para un mejor resultado, entregando = (10, 119)

## Parte 4: Reducción con SVD (LSA)

from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=2)
X_reducido = svd.fit_transform(X)

print(X_reducido)

### Resultados

- (10, 119)
- [[ 3.92202780e-01  6.20577578e-01]
-  [ 1.40410475e-01 -1.01447354e-01]
-  [ 1.04369777e-15 -2.62330150e-15]
-  [ 2.53782191e-01  6.39764241e-01]
-  [ 7.20083816e-01 -3.30755787e-01]
-  [-1.33832308e-16 -2.59690054e-15]
-  [-3.99006049e-16 -3.40865591e-15]
-  [ 1.57825750e-01  4.27280964e-01]
-  [ 2.82965943e-02 -3.04914557e-02]
-  [ 7.11302865e-01 -3.09165063e-01]]

## Parte 5: Análisis

### Responde:
- ¿Qué representan las nuevas dimensiones?
- ¿Se agrupan documentos similares?
- ¿Qué diferencias hay respecto a la reducción manual?

### Respuestas

- Representan componentes especiales que otorgan un cierto valor a los textos dependiendo de que tan relacionado se encuentre a los componentes, por decirlo de un modo y bajo el ejemplo. Como esta dividido en dos dimensiones, una de ellas captura un patrón importante entre palabras relacionadas, mientras que el segundo captura otro patrón distinto, teniendo un estandar para el resto de palabras, asi para cuando existe alguna comparativa, se tenga un valor que los relacione.
- Sí, los documentos similares tienden a agruparse en el espacio reducido. Por ejemplo, los documentos relacionados con inteligencia artificial y aprendizaje digital presentan coordenadas cercanas, indicando similitud después de la reducción de dimensionalidad mediante SVD.
- La mayor diferencia que hay es que, al hacerlo manual, por medio del ojo visual, identificamos de forma inmediata los conceptos que consideramos mas importantes y por medio de estos y de sus definiciones es que podemos relacionarlos, en cambio, con esto ya se puede tener valores que nos puedan ayudar a identificar que documentos son mas relacionados con cierto tema que otros.

## Parte 6: Comparación

| Aspecto | Manual | TF-IDF + SVD |
|---------|--------|--------------|
| Facilidad | ... | ... |
| Precisión | ... | ... |
| Escalabilidad | ... | ... |
| Objetividad | ... | ... |

### Resultado

| Aspecto | Manual | TF-IDF + SVD |
|---------|--------|--------------|
| Facilidad | Facil, unicamente es seleccionar palabras que se identifiquen como importantes | Facil, ya existen diversas librerias que se encargan de lo pesado, lo unico es recopilar la informacion correspondiente |
| Precisión | Complicada, en ocasiones, si no se conoce bien los conceptos, se puede afiliar informacion con terminos que no estan relacionados | Mayor, debido a los diferentes calculos que conlleva, vuelve mas agil la valoracion de los terminos afiliandolos con mayor precision al resto de terminos |
| Escalabilidad | Limitada, como solo conlleva la vision de la persona y de su entendimiento, no hay mucho que se le pueda agregar, mas que investigar mas sobre los terminos | Alta, entre mas terminos cuente las dimensiones o inclusive la cantidad de dimensiones puede aumentar la precision en la que afiliamos los terminos usados y buscados |
| Objetividad | Limitada, usualmente y aunque no se haga con intenciones, las personas solemos actuar con emociones, por lo que no siempre se tendra un analisis totalmente objetivo | Muy objetivo, al ser codigo regido por reglas es mas propenso a seguir las instrucciones que se le indiquen, por lo que el codigo no tomara ningun tipo de emocion al tomar una eleccion, solo calculos |

## Reflexión Final

- ¿Qué método es más confiable?
- ¿Cuál usarías en un sistema real?
- ¿Se pierde información en ambos casos?

### Respuestas

- Ambos metodos cuentan con sus buenas y malas y, considero que es situacional, para casos donde es limitada la informacion, donde solo se cuente con una cantidad minima de terminos y temas, el metodo manual podria ser mas confiable, la falta de informacion afectaria las desicion del sistema, volviendolo poco preciso. Caso contrario, si se tiene mucha informacion, con demasiados terminos y temas, el sistema sin duda seria la mejor opcion, ya que tendria mayor cantidad de datos con las cuales trabajar, ademas de que no se cansaria de analisar la informacion como lo haria una persona real. Para un caso realista, sin duda, el uso del sistema seria lo mas correcto a tomar en cuenta.
- La eleccion del uso de TF-IDF y SVD y demas elementos que conlleve el sistema seria una eleccion mas realista, analizar toda la informacion y datos llegaria a ser sumamente pesado, agotador y poco eficiente si lo hiciera una persona, costoso inclusive si se involucrara mas personas, el uso del sistema disminuiria por completo las desventajas y aprovecharia las ventajas.
- No sabria decir con toda la verdad que en ambos casos se perderia informacion, pero podria afirmar que, por lo menos, en el metodo manual, si que habria perdida de informacion conforme esta aumentase.

## Actividad Extra

- Probar con diferentes valores: ncomponents = 2, 3, 5
- Analizar cambios en resultados
- Agrupar documentos similares

### n components = 3

- (10, 119)
- [[ 3.92202780e-01  6.20577578e-01  9.35832705e-16]
-  [ 1.40410475e-01 -1.01447354e-01  1.61259925e-14]
-  [ 9.80862406e-16 -8.41203668e-16 -4.57225370e-15]
-  [ 2.53782191e-01  6.39764241e-01  1.81543083e-15]
-  [ 7.20083816e-01 -3.30755787e-01 -8.34787626e-16]
-  [ 1.51222706e-16 -2.90330019e-17  7.31937523e-01]
-  [-4.03729847e-16 -7.66296501e-16  7.31937523e-01]
-  [ 1.57825750e-01  4.27280964e-01 -1.15465291e-15]
-  [ 2.82965943e-02 -3.04914557e-02  1.18500398e-14]
-  [ 7.11302865e-01 -3.09165063e-01 -3.47904649e-15]]

### n components = 5

- (10, 119)
- [[ 3.92202780e-01  6.20577578e-01 -9.92570115e-16  2.98537999e-03 5.10390710e-16]
-  [ 1.40410475e-01 -1.01447354e-01 -1.01876182e-14  7.09576387e-01 -3.45984586e-15]
-  [-2.88843571e-16  1.66784824e-15  2.92558721e-15  4.37848039e-15 1.00000000e+00]
-  [ 2.53782191e-01  6.39764241e-01 -1.45344551e-15  3.21865474e-02 1.82351365e-15]
-  [ 7.20083816e-01 -3.30755787e-01  1.78114873e-15 -3.40215939e-02 6.78910314e-16]
-  [-4.86613126e-16  1.37963196e-15  7.31937523e-01  8.83882516e-15 -3.80465230e-15]
-  [-3.85161720e-16  1.28036743e-15  7.31937523e-01  1.33193465e-14 -5.58603880e-16]
-  [ 1.57825750e-01  4.27280964e-01 -8.03118946e-16  2.97874163e-02 -7.13564617e-15]
-  [ 2.82965943e-02 -3.04914557e-02 -1.15867495e-14  7.25542719e-01 -2.40299907e-15]
-  [ 7.11302865e-01 -3.09165063e-01  2.72456159e-15 -1.54230245e-01 1.32423077e-15]]

### Cambios en Resultados

Para el caso de la tercer dimension:
- Comenzó a separar documentos económicos y ambientales del resto.

Ventajas:
- Mejor separación temática,
- Menos pérdida de información,
- Representación más estable.

Para el caso de la quinta dimension:
- Los documentos tienen una representación mucho más específica.
- Documento 3 (fútbol) aparece prácticamente aislado en una dimensión exclusiva.
- El modelo detectó que ese documento contiene vocabulario muy diferente del resto.

Ventajas:
- Mayor capacidad para distinguir temas.
- Menor pérdida de información.

Desventaja:
- Al aumentar dimensiones, se reduce la compresión.
- El modelo comienza a parecerse más a la representación original TF-IDF.

### Agrupacion

**Grupo 1 — Inteligencia artificial y tecnología**

Documentos:
- Documento 1
- Documento 4
- Documento 8

Temas:
- Inteligencia artificial,
- Aprendizaje automático,
- Redes neuronales,
- Análisis de datos.

Evidencia:
- Presentan coordenadas similares en las primeras dimensiones.

**Grupo 2 — Educación digital**

Documentos:
- Documento 5
- Documento 10

Temas:
- Aprendizaje en línea,
- Plataformas digitales,
- Tecnología educativa.

Evidencia:
- Coordenadas muy cercanas en los componentes principales.

**Grupo 3 — Salud y bienestar**

Documentos:
- Documento 2
- Documento 9

Temas:
- Salud pública,
- Prevención de enfermedades,
- Alimentación saludable.

Evidencia:
- Aparecen relacionados especialmente cuando el numero de componentes es igual a 5.

**Grupo 4 — Temas aislados**

Documentos:
- Documento 3 → fútbol.
- Documento 6 → cambio climático.
- Documento 7 → inflación.

Características:
- Contienen vocabulario especializado y diferente del resto.
- Por ello el modelo los separa en dimensiones específicas.