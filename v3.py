from GUI import GUI
from HAL import HAL
import cv2 
import numpy as np

# Parámetros del controlador PID angular
Kp_angular = 1.3
Ki_angular = 0.0001
Kd_angular = 2.5

# Parámetros del controlador PID lineal
Kp_lineal = 1.3
Ki_lineal = 0.0001
Kd_lineal = 2.5

# Valores iniciales de las variables del controlador PID angular
error_prev_angular = 0
error_integral_angular = 0

# Valores iniciales de las variables del controlador PID lineal
error_prev_lineal = 0
error_integral_lineal = 0

# Función para calcular la señal de control PID
def calculate_pid_angular(error):
    global error_integral_angular
    global error_prev_angular
    
    # Término proporcional
    P = Kp_angular * error
    
    # Término integral
    error_integral_angular += error
    I = Ki_angular * error_integral_angular
    
    # Término derivativo
    D = Kd_angular * (error - error_prev_angular)
    
    # Calcular la señal de control
    control_signal = P + I + D
    
    # Actualizar el error previo
    error_prev_angular = error
    
    return control_signal

def calculate_pid_liner(error):
    global error_integral_lineal
    global error_prev_lineal
    
    # Calcula los términos PID inversos
    P = Kp_lineal * error

    error_integral_lineal += error
    I = -Ki_lineal * error_integral_lineal
    D = -Kd_lineal * (error - error_prev_lineal)

    # Calcula la salida del controlador PID inverso
    output = P + I + D

    # Actualiza el error previo para la próxima iteración
    error_prev_lineal = error

    return output

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

    w = calculate_pid_angular(error)
    v = calculate_pid_liner(error)
    
    HAL.setW(w)
    HAL.setV(v)
    
    GUI.showImage(img)