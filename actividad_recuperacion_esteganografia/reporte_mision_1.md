# **Misión 1: El Píxel Chismoso (Investigación y LSB Básico)**

**¿Qué es la Esteganografía?**

 Es la práctica de ocultar información dentro de otro mensaje u objeto físico para evitar su detección. Se puede usar para ocultar casi cualquier tipo de contenido digital, ya sea texto, imágenes, videos o audios. Luego, dichos datos ocultos se extraen en destino.

 A veces, el contenido encubierto mediante esteganografía se cifra antes de ocultarlo dentro de otro formato de archivo. Si no está cifrado, es posible que se procese de alguna manera para que sea más difícil de detectar.

 **¿Cómo funciona específicamente la técnica LSB en los píxeles de una imagen?**

La esteganografía consiste en ocultar información de forma que no se levanten sospechas. Una de las técnicas más comunes es la esteganografía de "bits menos significativos" (LSB). Consiste en incrustar la información secreta en los bits menos significativos de un archivo multimedia. Por ejemplo:

>- En un archivo de imagen, cada píxel está formado por tres bytes de datos correspondientes a los colores rojo, verde y azul. Algunos formatos de imagen asignan un cuarto byte adicional a la transparencia o "alfa".
>- La esteganografía de LSB modifica el último bit de cada uno de estos bytes para ocultar un bit de datos. Por lo tanto, para ocultar un megabyte de datos con este método, se necesitaría un archivo de imagen de ocho megabytes.
>- Modificar el último bit del valor del píxel no produce un cambio perceptible con notoriedad en la imagen, lo que significa que cualquier persona que vea la imagen original y la modificada con esteganografía no podrá diferenciarlas.

Tomemos como ejemplo un byte de valor 160. Su representación en binario es la siguiente:

1	0	1	0	0	0	0	**0**

Se ha marcado en negrita el bit menos significativo (LSB), que en este caso tiene el valor 0. Es decir, que este byte, tiene incrustado un bit de mensaje de valor 0. Si este es el valor que queremos incrustar, no será necesario realizar ninguna operación. Pero si el valor del bit del mensaje que queremos incrustar es el 1, tendremos que realizar una operación sobre el valor del byte que cambie su LSB.

Cuando se trata de incrustar información en el bit menos significativo de un byte existen dos técnicas habituales: el LSB replacement y el LSB matching. La primera de ellas y más frecuente es una técnica insegura, para la que existen múltiples ataques y que consiste, simplemente, en sustituir el valor del LSB por el valor del mensaje.

Continuando con el ejemplo anterior, para incrustar un 1 en un byte con valor 160:

1	0	1	0	0	0	0	**0**

Lo único que tendremos que hacer es sustituir el LSB por 1:

1	0	1	0	0	0	0	**1**

Esta técnica se conoce como LSB replacement y no se recomienda su uso por ser detectable. En el apartado “Los peligros del LSB replacement” se explica qué hace a esta técnica insegura.

Otra forma de modificar el LSB consisten sumar 1 o restar 1 al valor del byte. Por ejemplo, sumar 1 a:

1	0	1	0	0	0	0	0

Nos dará como resultado:

1	0	1	0	0	0	0	1

Mientras que al restar uno obtendremos:

1	0	0	1	1	1	1	1

En ambos casos hemos modificado el LSB, por lo que ambos casos llevan incrustado un 1 como valore del mensaje. El segundo caso, sin embargo, ha supuesto modificar 5 bits. Pero esto no debe considerarse más inseguro, puesto que en ambos casos hemos modificado el valor del byte en una unidad.

Esta técnica se conoce como LSB matching o incrustación ±1 y es mucho más segura que la anterior.

Incrustación de la información con LSB replacement

Supongamos que disponemos de los siguientes valores, correspondientes a un grupo de bytes obtenidos del medio digital en el que queremos ocultar el mensaje:

160	60	53	128	111	43	84	125

Si obtenemos su valor en binario tenemos:
| tabla | tabla | tabla | tabla |
|:--------:|:--------:|:--------:|:--------:|
| 10100000 | 00111100 | 00110101 | 10000000 |
| 01101111 | 00101011 | 01010100 | 01111101 |

Supongamos ahora que queremos ocultar un byte, por ejemplo el correspondiente al valor de la letra ‘A’ en codificación ASCII. Este valor corresponde al número 65, cuya representación en binario es la siguiente:

0	1	0	0	0	0	0	1

Lo haremos sustituyendo el valor del bit menos significativo de cada valor:

| tabla | tabla | tabla | tabla |
|:--------:|:--------:|:--------:|:--------:|
| 1010000**0** | 0011110**0** | 0011010**1** | 1000000**0** |
| 0110111**1** | 0010101**1** | 0101010**0** | 0111110**1** |

De manera que nos quedarán los siguientes valores:

160	61	52	128	110	42	84	125

En los inicios de la esteganografía en imágenes digitales se pensó erróneamente que esta era la forma más apropiada de esconder información, puesto que modificaba únicamente un bit. Desde un punto de vista intuitivo tiene mucho sentido, puesto que esta técnica nos permite insertar un bit de información modificando el valor del byte lo mínimo posible. Sin embargo esta operación introduce cambios significativos en la distribución estadística de los bytes, lo que la hace muy detectable.

Extracción de la información
Para extraer el mensaje únicamente tenemos que leer el LSB de los valores de los bytes correspondientes al medio que contiene el mensaje. El mismo procedimiento es válido para leer datos incrustados con LSB replacement y con LSB matching.

Veamos como realizar esta operación usando Python. Primero extraemos los bits:

>- message_bits = [ s%2 for s in stego ]

En este caso, la variable stego contiene los valores de los bytes extraídos del medio.

Ahora tenemos que agrupar los bits de 8 en 8 para formar el valor de los bytes del mensaje original:

message_ex = []
value = 0
for i in range(len(message_bits)):
    if i%8==0 and i!=0:
        message_ex.append(value)
        value = 0
    value |= message_bits[i] << i%8

import cv2
import numpy as np

## Codigo Implementado

>- img = cv2.imread('evidencia_1.png', cv2.IMREAD_GRAYSCALE)

- **2. Aplanado de la imagen**
- **------------------------------------------------------------**
- **La imagen originalmente es una matriz 2D (alto x ancho).**
- **flatten() convierte todos los píxeles en un solo vector**
- **para poder recorrerlos secuencialmente.**

>- pixels = img.flatten()

- **3. Extracción del bit menos significativo (LSB)**
- **------------------------------------------------------------**
- **Cada píxel tiene 8 bits. El mensaje oculto está almacenado**
- **en el último bit de cada píxel.**
- **La operación bit a bit:**
- **pixel & 1**
- **permite obtener únicamente ese último bit.**
>- bits = [p & 1 for p in pixels]

>- mensaje = ""
>- byte = 0
>- contador = 0

- **4. Reconstrucción de caracteres**
- **------------------------------------------------------------**
- **Cada 8 bits corresponden a un carácter ASCII.**
- **Los bits se van acumulando hasta completar un byte.**
>- for bit in bits:

    # Construcción del byte desplazando a la izquierda
    # y agregando el nuevo bit al final.
    byte = (byte << 1) | bit
    contador += 1

    # Cuando se juntan 8 bits se obtiene un carácter
    if contador == 8:
        caracter = chr(byte)
        mensaje += caracter

        # ----------------------------------------------------
        # 5. Condición de parada
        # ----------------------------------------------------
        # El ejercicio indica que el mensaje termina cuando
        # aparece la palabra clave ###FIN###
        if "###FIN###" in mensaje:
            break

        byte = 0
        contador = 0

>- print("Mensaje encontrado:")
>- print(mensaje)

## Aplanamiento de la imagen

Las imágenes normalmente se almacenan como matrices de dos dimensiones (alto × ancho). Para analizar todos los píxeles de forma secuencial, se utiliza:

>- pixels = img.flatten()

Esto transforma la matriz en un vector unidimensional que contiene todos los valores de los píxeles.

## Extracción del bit menos significativo

El mensaje oculto se encuentra en el último bit de cada píxel, conocido como LSB (Least Significant Bit). Para obtenerlo se utiliza:

>- pixel & 1

## Reconstrucción de bytes

Cada 8 bits forman un carácter ASCII. El byte se reconstruye utilizando desplazamientos de bits:

>- byte = (byte << 1) | bit

Esto desplaza el byte actual hacia la izquierda e inserta el nuevo bit en la posición menos significativa.

## Conversión a caracteres

Cuando se acumulan 8 bits, se convierten a un carácter ASCII usando:

>- chr(byte)

## Finalización de la lectura

El proceso continúa hasta encontrar la palabra clave:

>- ###FIN###

Esto evita seguir interpretando bits del resto de la imagen que no forman parte del mensaje.

## Nota importante sobre el orden de los bits (error común)

Durante el desarrollo del algoritmo se identificó un problema relacionado con el orden en que se reconstruyen los bits del byte.

Existen dos formas comunes de reconstruir un byte:

Método 1

>- byte |= bit << posicion

Este método funciona cuando el mensaje fue almacenado desde el bit menos significativo hacia el más significativo.

Ejemplo de orden:

>- bit0 bit1 bit2 bit3 bit4 bit5 bit6 bit7

Método 2

>- byte = (byte << 1) | bit

Este método reconstruye el byte desde el bit más significativo hacia el menos significativo.

Orden:

>- bit7 bit6 bit5 bit4 bit3 bit2 bit1 bit0

En este ejercicio, el mensaje fue almacenado utilizando este segundo esquema, por lo que el primer método producía caracteres incorrectos o ruido.

1. **Sobre la Investigación (Misión 1):** Explica con tus propias palabras qué es la Esteganografía LSB. ¿Por qué cambiar el último bit de un píxel no altera la imagen de forma visible para el ojo humano?

Dado que la esteganografia es una practica para ocultar algo a simple vista y LSB es el bit menos significativo, se podria definir todo junto como una practica que se apoya de los bits para ocultar mensajes, como es en este caso un texto sobre una imagen y, es totalmente posible por como funcionan las imagenes.

Las imagenes cuenta con muchos pixeles, pixeles que juntos forman imagenes, entre mas pixeles tenga la imagen mejor luce esta, hoy en dia hemos llegado a un punto en donde es necesario tener dos imagenes de resoluciones altas para poder notar las diferencias que tienen, cosa que antes se podia sin tener necesariamente las imagenes en el momento, esto combinado con el hecho de que, para un color ubicado en el pixel utiliza una serie de bits que forman un digito decimal que identifica a un color, este digito decimal abarca un espacio de mas 150 tonalidades que dependiendo de si son tonos grises o a color (RGB), pueden darle brillo u opacidad, cuando se trata de LSB en un pixel solo trata de aumentar o disminuir un bit a la serie de bits que tiene el pixel, por lo que el valor decimal, solo aumentaria o bajaria en 1 al pixel, esto es un valor muy pequeño como para notar su diferencia a distancia, aun mas, cuando los pixeles adyacentes o alrededor no llegan a alterarse por ser innecsarios para la causa, por lo que, tener que ubicar un pixel en una imagen que podria tener 300 o mas pixeles a lo largo y a lo ancho y, tener que diferenciarlo del resto de pixeles que pueden o no haber sido afectados por esto, resultaria muy complicado para un persona, por lo que a simple vista, esto no podria notarse (A menos que la imagen cuente con una cantidad de pixeles que sea clara para el ojo humano).