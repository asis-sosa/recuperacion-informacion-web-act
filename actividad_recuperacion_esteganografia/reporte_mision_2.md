# Misión 2: Operación Camaleón (Recuperación por Color HSV)

## ¿Como funciona RGB en una imagen?

RGB es un modelo de color basado en la síntesis aditiva, con el que es posible representar un color mediante la mezcla por adición de los tres colores de luz primarios. El modelo de color RGB no define por sí mismo lo que significa exactamente rojo, verde o azul, por lo que los mismos valores RGB pueden mostrar colores notablemente diferentes en distintos dispositivos que usen este modelo de color.

Los que generalmente se usan en el mundo digital son los espacios de color RGB, que significa Rojo, Verde y Azul en inglés. Eso significa que todos los colores en ese espacio son creados por alguna combinación de esos tres colores.

### Síntesis aditiva de color

Es un modelo que permite explicar la obtención de un color a partir de la suma de los componentes de color. El proceso de reproducción aditiva normalmente utiliza luz roja, verde y azul como componentes para producir el resto de colores. Combinando uno de estos colores primarios con otro en proporciones iguales se obtienen los colores aditivos secundarios: cian, y se pueden encontrar colores básicos magenta y amarillo. Combinando los tres colores primarios de luz con las mismas intensidades, se produce el blanco. Variando la intensidad de cada luz de color finalmente deja ver el espectro completo de estas tres luces.

## ¿Como funciona HSV en una imagen?

Es un modelo de color que representa los colores en términos de tono (tipo de color), saturación (intensidad del color) y valor (brillo).

En ella el matiz se representa por una región circular; una región triangular separada, puede ser usada para representar la saturación y el valor del color. Normalmente, el eje horizontal del triángulo denota la saturación, mientras que el eje vertical corresponde al valor del color. De este modo, un color puede ser elegido al tomar primero el matiz de una región circular, y después seleccionar la saturación y el valor del color deseados de la región triangular.

>- Ventajas del HSV: Facilita la selección y manipulación del color de manera más intuitiva en comparación con otros modelos como RGB.
>- Aplicaciones en Detección de Imágenes: El HSV es útil para la segmentación de imágenes basada en color debido a su capacidad para separar la información del color de la luminancia.

A diferencia del modelo RGB, que se basa en la combinación de rojo, verde y azul, el HSV se alinea más con la forma en que los humanos perciben el color.

>- Intuitividad: El HSV se alinea mejor con la percepción humana del color, facilitando la selección y ajuste de colores de manera más intuitiva. En RGB, cambiar un color específico requiere ajustar las tres componentes (rojo, verde, azul), lo que puede ser complicado.
>- Separación de Luminancia y Crominancia: El HSV separa la información del color (tono y saturación) de la información del brillo (valor). Esto es útil en aplicaciones de procesamiento de imágenes donde es necesario ajustar el color sin afectar el brillo, o viceversa.
>- Facilidad de Segmentación: El HSV facilita la segmentación de imágenes basada en color. Al definir rangos de tono y saturación, es posible aislar objetos de un color específico de manera más precisa que con RGB.
>- Menor Sensibilidad a Cambios de Iluminación: El HSV es menos sensible a los cambios de iluminación que el RGB. Esto significa que los colores en una imagen HSV son más consistentes bajo diferentes condiciones de luz.

2. **Sobre los Espacios de Color (Misión 2):** Intenta aislar el texto de la Misión 2 usando directamente los canales BGR. ¿Por qué crees que es casi imposible recuperar esa información en BGR, pero resultó tan fácil usando el canal 'H' (Hue) del modelo HSV?

Dado que el modelo RGB consiste en combinaciones de colores, para obtener uno solo, se podria considerar muy dificil descubrir las conbinaciones que se involucraron para poder crear ese color, quizas sea posible, pero se llevaria mucho tiempo descubrirlo, caso que no pasa con HSV ya que este ya cuenta por definido el rango de color (Tono o 'H') en sus caracteristicas, por lo que ubicar un color o tono seria mas sencillo.