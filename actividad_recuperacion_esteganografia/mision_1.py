import cv2
import numpy as np

# Cargar imagen en escala de grises
img = cv2.imread('evidencia_1.png', cv2.IMREAD_GRAYSCALE)

# 1. Aplanar imagen
pixels = img.flatten()

# 2. Extraer LSB
bits = [p & 1 for p in pixels]

mensaje = ""
byte = 0
contador = 0

# 3. Reconstrucción de bytes
for bit in bits:

    byte = (byte << 1) | bit
    contador += 1

    if contador == 8:
        caracter = chr(byte)
        mensaje += caracter

        # detener cuando aparezca ###FIN###
        if "###FIN###" in mensaje:
            break

        byte = 0
        contador = 0

print("Mensaje encontrado:")
print(mensaje)