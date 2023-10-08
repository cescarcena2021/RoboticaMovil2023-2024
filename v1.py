from GUI import GUI
from HAL import HAL
import cv2  # Importar OpenCV
import numpy as np

cx = 0 
cy = 0

# Parámetros del controlador PID (ajusta estos valores según sea necesario)
Kp = 0.1  # Ganancia proporcional
Ki = 0.01  # Ganancia integral
Kd = 0.05  # Ganancia derivativa

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

while True:
    image = HAL.getImage()
    GUI.showImage(image)
  
    image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Filtrar el color rojo en la imagen
    lower_red = (0, 0, 100)
    upper_red = (100, 100, 255)
    
    mask = cv2.inRange(image_cv, lower_red, upper_red)
    mask = cv2.bitwise_not(mask)

    high, width, deep = image.shape

    M = cv2.moments(mask)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        # Calcular el error en la posición horizontal
        error = cx - width/2
        print(error)
        
    W = calculate_pid_control(error)
    #print(error)
    
    # Aplicar las velocidades al robot
    HAL.setV(4)
    HAL.setW(W)
           
    # Enter iterative code!
