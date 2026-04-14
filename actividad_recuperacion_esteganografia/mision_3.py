import cv2
import numpy as np

img = cv2.imread("evidencia_3.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Extraer canal Hue
hue = hsv[:,:,0]

lower = np.array([15, 100, 100])
upper = np.array([20, 255, 255])

mask = cv2.inRange(hsv, lower, upper)

# aplicar máscara para ver solo la tinta enemiga
lsb_filtrado = cv2.bitwise_and(img, img, mask=mask)

# ------------------------------------------------------------
# 5. Extraer los píxeles que cumplen la máscara
# ------------------------------------------------------------
pixels = hue[mask > 0]

# ------------------------------------------------------------
# 6. Obtener LSB de esos píxeles
# ------------------------------------------------------------
bits = [p & 1 for p in pixels]

mensaje = ""
byte = 0
contador = 0

for bit in bits:

    byte = (byte << 1) | bit
    contador += 1

    if contador == 8:
        caracter = chr(byte)
        mensaje += caracter

        if "###FIN###" in mensaje:
            break

        byte = 0
        contador = 0

print("Mensaje encontrado:")
print(mensaje)

# ------------------------------------------------------------
# Mostrar referencia
# ------------------------------------------------------------
cv2.imshow("Imagen original", img)
cv2.imshow("Mascara tinta enemiga", mask)
cv2.imshow("LSB del Hue filtrado", lsb_filtrado)

cv2.waitKey(0)
cv2.destroyAllWindows()
