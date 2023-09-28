# RoboticaMovil2023-2024 🤖​

## Paractica 1 📍

Para esta primera practica habia diseñar el software de una asporadora para que esta funcionara sin odometria, es decir, sin tenir ningun tipo de referencia de donde se encuentra en el mapa. Para ello se pidio que hiceramos un software que fuera pseudoaleatorio. Para ello me puse manos a la obra con la pirmera version 

### Primera version 🕹️​
Esta version corresponde con el archivo first_version.py donde creamos la primera maquinas de estados con 3 estados, que seraian espiral, ir para delante e ir para detras. Rapidamente me di cuenta de que este primer portotipo tenia algunos errores y era muy sensible a fallos, por ello decidi hacer una segunda version 

### Segunda version 🎲​
Esta version corresponde con el archivo second_version.py. En esta version añadi un nuevo estado de giro que permite a robot tener merjor funcionamiento. Ademas de eso reajute los valores de las velocidades y hice que varias de estas tubieran caracter aleatorio.

### Version final 🏅​
Esta version corresponde con el archivo Final_version.py. En este archivo podemos encontrar el codigo final de la practica, que se se muestra en funcionamiento en el video. Para esta version final intente añadir un cuarto estado para cuando el robot estubiera en sitios muy pequemos, puesto que este perdia mucho tiempo alli. ESte estado consitia en que cuando el robot chocara varias veces con la pared en un periodo de tiempo, esto significaba que estaba atrapado. Por tanto devieria encontar la salida e ir hacia alli. Finalmente no lo pude realizar ya que tuve problemas con el bumper ya que el robot detectaba falsas colisiones y tambien tuve problemas con las patas de las sillas y mesas puesto que al laser le cuesta detectarlo.
Finalmente lo que hice fue reajustar valores de nuevo y cambiar el sentido del giro para optimizarlo todo y que pudiera llega a mas sitos.

Aqui podemos ver una foto de lo recorrido por el robot depues de aproximadamente unos 15 minutos

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/9c9a3ac7-7909-4365-8943-71ead89bbba2)

### Video de funcionamiento final 📽️

[Screencast from 09-28-2023 09:07:00 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/6ce9491a-1c7b-46a7-b1c4-cc7d89465a4a)


