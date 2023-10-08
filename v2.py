from GUI import GUI
from HAL import HAL
import cv2 
import numpy as np

Kp = 0.91
Ki = 0.000000002
Kd = 0.777
D_iter = 5
E_iter = 1


# Parámetros del controlador PID (ajusta estos valores según sea necesario)
# Kp = 0.1  # Ganancia proporcional
# Ki = 0.01  # Ganancia integral
# Kd = 0.05  # Ganancia derivativa

# Valores iniciales de las variables del controlador PID
error_prev = 0
error_integral = 0

# Función para calcular la señal de control PID
def calculate_pid_control(error):
    global error_integral
    global error_prev
    
    # Término proporcional
    P = Kp * error
    
    # Término integral
    error_integral += error
    I = Ki * error_integral
    
    # Término derivativo
    D = Kd * (error - error_prev)
    
    # Calcular la señal de control
    control_signal = P + I + D
    
    # Actualizar el error previo
    error_prev = error
    
    return control_signal

HAL.setV(4)

while True:
    # Enter iterative code!
    img = HAL.getImage()
    height, width, channel = img.shape

    # image process to make the imgae more smooth so that we can obtain more information
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv, (5,5), 0)

    # Filtrar el color rojo en la imagen
    lower_red = (0, 43, 46)
    upper_red = (26,255,255)

    # detect the color of line
    res = cv2.inRange(blur, lower_red, upper_red)
    # d = cv.dilate(res, kernel=keneral, iterations=D_iter)
    # e = cv.erode(d, kernel=keneral, iterations=E_iter)

    # caculate the center of the line
    m = cv2.moments(res)
    cx = int(m['m10']/m['m00'])
    cy = int(m['m01']/m['m00'])

    cv2.circle(img,(cx,cy),20,(100,100,100),-1)
    
    # position PID control
    error = -(cx - width/2)/300

    angular = calculate_pid_control(error)
    
    
    HAL.setW(angular)
    
    GUI.showImage(img)