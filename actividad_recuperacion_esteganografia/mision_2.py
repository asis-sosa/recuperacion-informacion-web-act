import cv2
import numpy as np

# ------------------------------------------------------------
# 1. Cargar imagen
# ------------------------------------------------------------
img = cv2.imread("evidencia_2.png")

# ------------------------------------------------------------
# 2. Convertir de BGR a HSV
# ------------------------------------------------------------
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# ------------------------------------------------------------
# 3. Definir rango de Matiz (Hue) de la tinta enemiga
# Solo filtramos Hue; S y V quedan abiertos
# ------------------------------------------------------------
lower = np.array([60, 0, 0])
upper = np.array([70, 255, 255])

# ------------------------------------------------------------
# 4. Crear máscara
# ------------------------------------------------------------
mask = cv2.inRange(hsv, lower, upper)

# ------------------------------------------------------------
# 5. Aplicar la máscara para revelar el texto
# ------------------------------------------------------------
result = cv2.bitwise_and(img, img, mask=mask)

# ------------------------------------------------------------
# 7. Mostrar resultados
# ------------------------------------------------------------
cv2.imshow("Imagen original", img)
cv2.imshow("Mascara (pixeles Hue 63-66)", mask)
cv2.imshow("Resultado filtrado", result)

cv2.waitKey(0)
cv2.destroyAllWindows()