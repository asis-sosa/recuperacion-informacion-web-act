# **Expediente X: Recuperación de la Información y Esteganografía**

## **Introducción para los Agentes**

La Recuperación de la Información (IR) no siempre consiste en buscar texto en una base de datos. A veces, la información está oculta a plena vista dentro de archivos multimedia. Su misión de hoy consta de tres fases para recuperar datos clasificados.

## **Misión 1: El Píxel Chismoso (Investigación y LSB Básico)**

**La Historia**

Hemos interceptado una imagen en escala de grises (evidencia_1.png). Nuestros analistas aseguran que contiene un mensaje de texto oculto mediante una técnica llamada Esteganografía LSB (Least Significant Bit).

**Tu Tarea**

>- **Fase de Investigación:** Antes de programar, investiga en internet: ¿Qué es la Esteganografía? ¿Cómo funciona específicamente la técnica LSB en los píxeles de una imagen?
>- **Fase de Extracción:** Sabiendo que el mensaje está en el último bit de cada píxel, aplana la imagen, extrae el bit menos significativo de cada valor (usando la operación bit a bit & con 1), agrúpalos de 8 en 8 (un byte), conviértelos a caracteres ASCII y detente cuando encuentres la palabra clave ###FIN###.

>- import cv2
>- import numpy as np

>- Cargar la imagen interceptada (en escala de grises)
>- img = cv2.imread('evidencia_1.png', cv2.IMREAD_GRAYSCALE)

>- ESCRIBE TU CÓDIGO AQUÍ:
>- Aplanar la imagen, extraer el último bit, agrupar en bytes y convertir a texto.

## Misión 2: Operación Camaleón (Recuperación por Color HSV)

**La Historia**

El enemigo se dio cuenta de que conocemos el método LSB y cambió de táctica. Interceptamos evidencia_2.png. Parece un simple fondo verde aburrido, pero contiene un texto escrito con "Tinta Camaleón". El texto tiene exactamente el mismo brillo y saturación que el fondo, pero alteraron ligeramente el Matiz (Hue). El ojo humano no lo ve, pero OpenCV sí.

**Las Pistas**

>- La imagen parece completamente verde (En HSV, el verde ronda el valor H=60).
>- La tinta enemiga tiene una frecuencia de Matiz ligeramente superior, alrededor de H=64.

**Tu Tarea**

Convierte la imagen de BGR a HSV y utiliza cv2.inRange para crear una "máscara" que filtre y recupere solamente los píxeles que estén en el rango de la tinta enemiga (por ejemplo, entre H=63 y H=66).

>- Cargar evidencia_2.png
>- Convertir a HSV
>- Aplicar cv2.inRange para revelar el mensaje

## Misión 3: El Cifrado Cromático (El Reto Híbrido HSV + LSB)

**La Historia**

¡El reto final! El enemigo ha combinado ambas técnicas en evidencia_3.png. Han ocultado un mensaje usando la técnica LSB, pero la información no está en toda la imagen. Los datos secretos están escondidos exclusivamente en los bits menos significativos del canal V (Value/Brillo) de los píxeles que pertenecen al color Amarillo Pardo.

**Las Pistas**

Llave de Color: Amarillo Pardo (Rango HSV sugerido -> Bajo: [15, 100, 100], Alto: [20, 255, 255]).
Debes crear una máscara para aislar ese color. Luego, extraer el LSB solo de los píxeles amarillos del canal V, agruparlos en ASCII y buscar el delimitador ###FIN###.

>- Cargar evidencia_3.png y convertir a HSV
>- Crear máscara para el Amarillo Pardo
>- Extraer canal V y obtener solo los píxeles donde la máscara es válida
>- Aplicar decodificación LSB a ese subconjunto de píxeles

## Entregable: Reporte de Misión (Formato Markdown)

Deben entregar un archivo reporte_mision.md con la siguiente estructura. Deberán incluir sus códigos, capturas de pantalla de los mensajes revelados, y responder a las preguntas del Análisis del Analista.

>- Reporte de Misión: Recuperación de la Información
**Agente Especial:** [Tu Nombre/Matrícula]

>- Misión 1, 2 y 3
[Incluir aquí los bloques de código Python y las imágenes o textos recuperados de cada misión]

>- Análisis del Analista (Reflexiones Finales)

1. **Sobre la Investigación (Misión 1):** Explica con tus propias palabras qué es la Esteganografía LSB. ¿Por qué cambiar el último bit de un píxel no altera la imagen de forma visible para el ojo humano?
> *[Tu respuesta]*

2. **Sobre los Espacios de Color (Misión 2):** Intenta aislar el texto de la Misión 2 usando directamente los canales BGR. ¿Por qué crees que es casi imposible recuperar esa información en BGR, pero resultó tan fácil usando el canal 'H' (Hue) del modelo HSV?
> *[Tu respuesta]*

3. **Sobre la Lógica de Recuperación (Misión 3):** Si en la Misión 3 intentaras extraer el mensaje LSB de toda la imagen completa (sin usar la máscara amarilla primero), ¿qué obtendrías como texto? ¿Cómo demuestra esto que el color actuó como una "llave de acceso"?
> *[Tu respuesta]*