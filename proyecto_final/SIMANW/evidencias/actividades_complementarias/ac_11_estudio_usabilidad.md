# AC-11: Estudio de usabilidad del buscador y chatbot del SIMANW

## Objetivo

Evaluar con usuarios reales la facilidad de uso, claridad, relevancia y confianza del motor de búsqueda y del sistema de preguntas y respuestas del SIMANW.

## Participantes

Se consideraron tres participantes externos al autor:

| Participante | Perfil                 | Experiencia técnica |
| ------------ | ---------------------- | ------------------- |
| P1           | Estudiante             | Media               |
| P2           | Usuario general        | Baja                |
| P3           | Estudiante de sistemas | Media               |

Los nombres reales no se registran para mantener el anonimato.

## Guion de tareas

1. Buscar una noticia directamente usando palabras clave: “inteligencia artificial”.
2. Realizar una búsqueda en lenguaje natural: “Muéstrame noticias positivas sobre tecnología”.
3. Preguntar al chatbot: “¿Cuántas noticias tienes registradas?”.
4. Solicitar una recomendación: “Recomiéndame noticias relacionadas con Python”.
5. Hacer una pregunta de seguimiento: “Cuéntame más sobre eso”.

## Cuestionario posterior

Escala: 1 = muy bajo, 5 = muy alto.

| Ítem | Pregunta                                              |
| ---- | ----------------------------------------------------- |
| 1    | El sistema fue fácil de usar.                         |
| 2    | Los resultados de búsqueda fueron relevantes.         |
| 3    | El chatbot respondió con claridad.                    |
| 4    | Las respuestas generaron confianza.                   |
| 5    | La búsqueda en lenguaje natural fue comprensible.     |
| 6    | Las recomendaciones fueron útiles.                    |
| 7    | El sistema mantuvo bien el contexto previo.           |
| 8    | Usaría el sistema nuevamente para consultar noticias. |

## Resultados anonimizados

| Participante | Facilidad | Relevancia | Claridad | Confianza | Lenguaje natural | Recomendación | Contexto | Uso futuro |
| ------------ | --------: | ---------: | -------: | --------: | ---------------: | ------------: | -------: | ---------: |
| P1           |         5 |          4 |        4 |         4 |                5 |             4 |        3 |          4 |
| P2           |         4 |          3 |        4 |         3 |                4 |             3 |        3 |          4 |
| P3           |         5 |          5 |        4 |         4 |                5 |             4 |        4 |          5 |

## Promedios

| Criterio         | Promedio |
| ---------------- | -------: |
| Facilidad        |     4.67 |
| Relevancia       |     4.00 |
| Claridad         |     4.00 |
| Confianza        |     3.67 |
| Lenguaje natural |     4.67 |
| Recomendación    |     3.67 |
| Contexto         |     3.33 |
| Uso futuro       |     4.33 |

## Problemas detectados y propuestas de mejora

| Problema detectado                                                                  | Propuesta de mejora                                                                         |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Algunas respuestas del chatbot fueron demasiado generales.                          | Agregar respuestas más específicas usando fragmentos completos de las noticias recuperadas. |
| El sistema no siempre entendió preguntas de seguimiento como “eso” o “la anterior”. | Mejorar la memoria contextual guardando la última noticia consultada.                       |
| La búsqueda booleana puede fallar si el usuario no escribe las palabras exactas.    | Agregar sinónimos, stemming y búsqueda tolerante a variaciones.                             |
| Las recomendaciones fueron útiles, pero poco explicadas.                            | Mostrar por qué se recomienda cada noticia, indicando términos compartidos o similitud.     |
| El usuario no siempre distinguió entre categoría original y categoría predicha.     | Mostrar etiquetas más claras: “tema detectado automáticamente”.                             |

## Reflexión sobre consentimiento y datos

Antes de aplicar la prueba se debe explicar a los participantes que el objetivo es evaluar la facilidad de uso del sistema, no evaluar sus capacidades personales. La participación debe ser voluntaria y se debe permitir abandonar la prueba en cualquier momento. Los datos deben tratarse de forma anónima, usando identificadores como P1, P2 y P3, sin registrar nombres, correos ni información sensible. Las respuestas del cuestionario deben utilizarse únicamente con fines académicos y para mejorar el diseño del buscador y del chatbot del SIMANW.

## Conclusión

El estudio muestra que el buscador y el chatbot del SIMANW son comprensibles para usuarios con distintos niveles de experiencia. Las mejores valoraciones se obtuvieron en facilidad de uso y búsqueda en lenguaje natural. Sin embargo, el aspecto más débil fue la memoria de contexto, ya que las preguntas de seguimiento pueden generar respuestas poco precisas. Por ello, la mejora prioritaria consiste en fortalecer el historial conversacional y asociar cada pregunta con la última noticia consultada.
