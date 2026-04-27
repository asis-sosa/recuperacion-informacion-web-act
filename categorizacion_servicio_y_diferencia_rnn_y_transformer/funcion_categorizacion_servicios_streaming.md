# Como Funciona la Categorizacion en los Servicios de Streaming - Amazon Prime, Neflix y Disney+

No hay una lista “oficial pública” donde Amazon Prime Video, Netflix o Disney+ digan exactamente todos sus algoritmos (eso es parte de su ventaja competitiva), Pero sí se sabe, por papers, ingeniería publicada y comportamiento del sistema, qué tipos de categorización y recomendación usa cada uno. Y aquí sí hay diferencias interesantes.

## Tipos mas Utilizados por los Servicios de Streaming

**El Sistema Analiza el Contenido o Categorización de Contenido.**

Para cada título se genera una ficha con muchísima información, por ejemplo:
- género → acción, drama, terror
- subgénero → thriller psicológico, sci-fi distópico
- duración
- año
- idioma
- país
- actores
- director
- clasificación por edad
- tono → oscuro, divertido, emotivo
- ritmo → lento, rápido
- temática → viajes en el tiempo, crimen, romance
- tipo de audiencia → familiar, adulto, juvenil

## Analiza el comportamiento del usuario para crear un perfil del usuario.

No solo registra qué viste, sino cómo lo viste:
- qué contenido abriste
- cuánto tiempo lo viste
- si terminaste la película
- si abandonaste a los 10 minutos
- si viste varios episodios seguidos
- si regresaste a ver algo similar
- búsquedas realizadas
- horarios de consumo
- dispositivos usados

## Busca usuarios parecidos a ti o collaborative filtering o filtrado colaborativo

“usuarios parecidos a ti también vieron esto”

| usuario | contenido visto |
|---------|-----------------|
| tu | Fallout, Reacher, The Boys |
| usuario B | Fallout, Reacher, The Boys, Invincible |

Entonces el sistema piensa:
- “si ambos tienen gustos similares, probablemente te guste Invincible”

## Busca contenido similar o content-based filtering o filtrado basado en contenido

Si viste The Lord of the Rings: The Rings of Power, el sistema busca títulos con características similares:
- fantasía épica
- aventura
- mundos medievales
- magia
- guerras

Entonces podría recomendar:
- The Wheel of Time
- Game of Thrones (si está disponible)
- otras series similares

## Sistema híbrido

combinan:
- comportamiento del usuario
- similitud entre usuarios
- similitud entre contenidos
- popularidad global
- tendencias recientes

Algo así: Recomendacion = gustos_usuario + usuarios_similares + contenido_similar + tendencias

## Curacion Humana

- La curación humana implica la selección, refinamiento y organización de información, experiencias o conocimientos con la guía de un experto. Sus características incluyen:
- Intervención activa: un experto evalúa qué información es relevante, confiable o significativa.
- Retroalimentación constante: los juicios del curador influyen en cómo se estructura y prioriza la información.
- Aprendizaje guiado: el curador basa las decisiones en experiencias previas, normas o principios reconocidos.
- Ejemplos: un médico diagnostica un paciente usando antecedentes clínicos y pruebas de laboratorio, seleccionando los datos más pertinentes para llegar a un juicio.

### Neflix

**Netflix es el referente en sistemas de recomendación.**

**Filtrado colaborativo**
- Usuarios similares → recomendaciones
- Base histórica muy grande

**Filtrado basado en contenido**
- Analiza características de películas/series

**Micro-categorización extrema**

Netflix tiene miles de categorías ocultas, por ejemplo:
- “comedias oscuras con protagonistas femeninas fuertes”
- “thrillers políticos basados en hechos reales”

Esto es más granular que cualquier otro servicio.

**Modelos de ranking personalizados**

No solo decide qué mostrar, sino:
- en qué orden
- en qué fila
- con qué portada (sí, cambia la imagen)

**Deep Learning / embeddings**
- Representa usuarios y contenido como vectores
- Calcula similitud matemática

**Contexto y tiempo**
- hora del día
- dispositivo
- si estás solo o en familia (inferido)

**El sistema más complejo, con fuerte uso de IA avanzada y personalización profunda.**

**Aprendizajes**

Usa los tres, pero destaca en no supervisado + supervisado + deep learning híbrido

**Supervisado**

Se usa cuando hay “etiquetas” claras:
- si viste algo completo → “te gustó”
- si abandonaste → “no te gustó”
- si le diste like/dislike

**No Supervisado**

Para descubrir patrones sin etiquetas:
- clustering de usuarios (grupos de gustos)
- clustering de contenido (películas similares)
- embeddings (vectores de similitud)

**Semi Supervisado**

Porque:
- no todos los datos tienen etiquetas claras
- combinan datos “con etiqueta” + “sin etiqueta”

### Amazon Prime

**Amazon Prime Video usa varias técnicas, pero con un enfoque distinto.**

**Filtrado colaborativo**
- Muy influenciado por Amazon (lo mismo que usa para productos):
- “usuarios que vieron esto también vieron…”

**Filtrado basado en contenido**
- géneros
- actores
- temas

**Metadatos enriquecidos**

Aquí destaca mucho:
- etiquetas manuales y automáticas
- tono, estilo, audiencia

Menos granular que Netflix, pero sólido.

**Integración con el ecosistema Amazon**

Esto es clave y lo diferencia:
- historial de compras
- búsquedas en Amazon
- intereses generales

**IA para “temas dinámicos”**
- categorías generadas automáticamente
- menos complejas que Netflix, pero más recientes

**Sistema híbrido sólido, menos sofisticado que Netflix, pero con ventaja en datos externos.**

**Aprendizajes**

Usa los tres, pero con énfasis en supervisado + sistemas híbridos clásicos

**Supervisado**
- predicción de qué verás
- basado en historial
- muy influenciado por el modelo de recomendaciones de Amazon (productos)

**No Supervisado**
- agrupación de contenido
- similitud entre usuarios
- menos profundo que Netflix

**Semi Supervisado**

mezcla de:
- metadatos (etiquetados)
- comportamiento (sin etiquetar directamente)

### Disney+

**Disney+ es diferente por estrategia.**

**Filtrado basado en contenido (principal)**
- franquicias (Marvel, Star Wars, Pixar)
- géneros básicos
- colecciones

**Curación editorial (muy importante)**

Aquí humanos deciden mucho:
- “colección de películas de villanos”
- “lo mejor de Marvel”

Esto reduce dependencia de IA.

**Filtrado colaborativo (limitado)**
- sí existe, pero menos dominante

**Popularidad y tendencias**
- lo más visto
- lo nuevo

**Menos IA compleja, más control humano y enfoque en franquicias.**

**Aprendizajes**

Predomina supervisado + curación humana, con menor uso de IA avanzada

**Supervisado**
- recomendaciones básicas
- popularidad
- historial del usuario

**No Supervisado**
- algo de agrupación
- menos dependencia de clustering avanzado

**Semi Supervisado**
- no es el enfoque principal

Disney+ usa mucho:

**curación humana (no es ML)**

Ejemplo:
- colecciones de Marvel
- listas temáticas hechas por editores