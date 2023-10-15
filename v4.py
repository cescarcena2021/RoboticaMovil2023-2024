from GUI import GUI
from HAL import HAL
import cv2 
import numpy as np

# Parámetros del controlador PID angular
Kp_angular = 1
Ki_angular = 0.0001
Kd_angular = 2.7

# Parámetros del controlador PID lineal
Kp_lineal = 0.85
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

def calculate_pid_lineal(error):
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


while True:
    # Enter iterative code!
    v = 5
    img = HAL.getImage()
    height, width, channel = img.shape

    y1 = 200
    y2 = 270
    
    y3 = 300
    y4 = 350
    
    franja_seleccionada = img[y1:y2, :]
    franja_seleccionada2 = img[y3:y4, :]


    # image process to make the imgae more smooth so that we can obtain more information
    hsv1 = cv2.cvtColor(franja_seleccionada, cv2.COLOR_BGR2HSV)
    blur1 = cv2.GaussianBlur(hsv1, (5,5), 0)

    hsv2 = cv2.cvtColor(franja_seleccionada2, cv2.COLOR_BGR2HSV)
    blur2 = cv2.GaussianBlur(hsv2, (5,5), 0)

    # Filtrar el color rojo en la imagen
    lower_red = (0, 43, 46)
    upper_red = (26,255,255)

    # detect the color of line
    res1 = cv2.inRange(blur1, lower_red, upper_red)
    res2 = cv2.inRange(blur2, lower_red, upper_red)
    # d = cv.dilate(res, kernel=keneral, iterations=D_iter)
    # e = cv.erode(d, kernel=keneral, iterations=E_iter)

    # caculate the center of the line
    m1 = cv2.moments(res1)
    if m1['m00'] > 0:
      cx1 = int(m1['m10']/m1['m00'])
      cy1 = int(m1['m01']/m1['m00'])

    m2 = cv2.moments(res2)
    if m2['m00'] > 0:
      cx2 = int(m2['m10']/m2['m00'])
      cy2 = int(m2['m01']/m2['m00'])

    cv2.circle(franja_seleccionada,(cx1,cy1),5,(255,0,0),-1)
    cv2.circle(franja_seleccionada2,(cx2,cy2),10,(255,0,0),-1)
    
    # position PID control
    error_angular = -(cx2 - width/2)/300
    error_lineal = -(cx1 - width/2)/300
    
    print(error_lineal)

    umbral_curva = 0.07
    
    if(abs(error_lineal) > umbral_curva):
      print("entra")
      w = calculate_pid_angular(error_angular)
      v = 4.3
      
    else:
      w = calculate_pid_lineal(error_lineal)
      v = 10
        
    HAL.setW(w)
    HAL.setV(v)

    GUI.showImage(img)