# Visual Follow Line 🏎️​

## Objetivo 🎯
El objetivo de este ejercicio es realizar un control reactivo PID capaz de seguir la línea pintada en el circuito de carreras.

## Percepción 👁️​
Para que el coche sea capaz de seguir una línea, primero tiene que tener información de en qué lugar se encuentra esta. Por ello, la primera aproximación a la práctica fue centrarse en la visión del coche y de qué forma detectaba la línea. El coche, como único sensor, posee una cámara incorporada en el chasis que nos permite ver en primera persona por dónde estamos yendo.
La primera idea que se me ocurrió fue hacer un filtro de color con OpenCV para que de toda la imagen solo lo importante fuera la línea roja. Una vez conseguido eso, el siguiente paso era detectar cuán lejos estaba la línea de la posición en la que estaba el coche, así que se me ocurrió utilizar el momento del polígono pintado por el filtro de color. El momento me daba el centro de este polígono, entonces podría saber si estoy muy desviado o poco desviado del centro de la línea. Todo funcionaba de forma correcta hasta que comenzaba a subir la velocidad en las curvas. A más de 5 de velocidad era imposible corregir la curva, y tras varios intentos me di cuenta de que donde el coche estaba tomando la referencia de la línea era demasiado cerca, por tanto era incapaz de reaccionar a las curvas hasta que nos estaba completamente dentro de ellas.
![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/338d2326-f0fe-47ff-b2f2-cd1cbb2291f2)


### Doble percepción 👀

Lo que se me ocurrió fue dividir la imagen para conseguir dos polígonos y sacar dos momentos, uno más próximo al coche y otro más lejano a él, de tal forma que el lejano fuera capaz de detectar curvas antes de estar dentro de ellas y el cercano fuera capaz de detectar la desviación de la línea cerca del coche.
![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/12707cfc-a8a9-43d6-85c8-5af499e22025)

## Un único PID

Al comenzar la práctica, como dice el enunciado, hay que implementar un PID, así que una vez logré la parte de percepción implementé un PID que controlará la velocidad angular del coche y le permitirá girar cuando lo necesite. Esto funcionaba de manera correcta pero no era óptimo, ya que no tenía ningún sentido ir a la misma velocidad en curvas que en rectas. Por tanto, decidí aplicar ese mismo PID a la velocidad lineal. Todo fue catastrófico y rápidamente me di cuenta de que necesitaba dos PID distintos.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/a0f9499f-8832-4f7f-b1b7-a6710cb4afcc)


## PID para curvas y PID para rectas

Tras la catástrofe, creé otro PID con valores distintos para que pudiera controlar la velocidad lineal. Pero tras muchos ajustes no era capaz de conseguir que el coche dejara de oscilar o de hacer cosas extrañas. Y la razón es que todo estaba causado por que el PID angular intentaba corregir un error a X velocidad y el lineal justo disminuía la velocidad también, entonces la corrección del angular era errónea. En conclusión, uno iba pisando al otro y viceversa.

Por tanto, se me ocurrió que en vez de un PID angular y otro lineal, podía hacer uno para rectas y otro para curvas. Así que me puse manos a la obra y elaboré estos dos PID y añadí una variable llamada umbral de curva que indica si estamos en una curva o no. Además de esto, fijé dos velocidades constantes que tenían mucho más sentido que una única velocidad. De esta manera, el coche funciona de manera muy correcta.

## Velocidad vs Seguridad ​🏁

Una vez tuve terminada toda la parte de código, tocaba ajustar velocidad y valores de PID. Estos tenían que ser lo suficientemente altos para permitir ir al coche a mayor velocidad y ser lo suficientemente seguros como para que el coche no chocara en ninguna curva cerrada o chicane. Además, estos valores tenían que ser robustos en cualquier tipo de circuito, no debían ser solo útiles en el circuito Simple.
Por ello, tras muchas pruebas en diferentes circuitos, el compromiso entre velocidad y seguridad que he encontrado ha sido:

| Circuito      | Velocidad 4.3 | Velocidad 4 |
| ------------- | ------------- | ------------|
| Simple  | 153s  |       165s      |
| Montmelo  | Failed  |    305         |
| Montreal  | Failed |  Die in chican|
| Nürburgring|  268 |  268 |

Circuito simple -> 135s
Montmelo -> 
Montreal ->
Nürburgring ->

### Objetivo cumplido ‼️​

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/d26031de-3822-4127-af6b-03fe0f97fb87)




