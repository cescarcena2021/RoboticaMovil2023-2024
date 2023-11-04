# Visual Follow Line 🏎️​

## Objetivo 🎯
El objetivo de este ejercicio es realizar un control reactivo PID capaz de seguir la línea pintada en el circuito de carreras.

## Navegacion VFF​
Para esta practica usaremos una tecnica de navegacion conocida como VFF .La idea detrás de est tecnica es crear un mapa local del entorno del robot y utilizarlo para generar un campo de vectores que indica la dirección en la que el robot debe moverse para evitar obstáculos y alcanzar su destino. Aquí hay un resumen de cómo funciona:

**Mapeo**: El robot utiliza sensores, como cámaras, láseres o ultrasonidos, para recopilar información sobre su entorno inmediato. A partir de estos datos, se construye un mapa local que representa la ubicación de obstáculos, paredes y otros objetos cercanos al robot.

**Generación del campo de vectores**: Se crea un campo de vectores en el que cada punto en el mapa local tiene un vector asociado. Este vector indica la dirección en la que el robot debe moverse desde ese punto para llegar a su destino y evitar obstáculos. Los vectores se generan de manera que el robot sea atraído hacia su objetivo y repelido por los obstáculos.

**Navegación**: El robot sigue los vectores del campo de vectores para navegar de manera autónoma. A medida que el robot se mueve, el campo de vectores se actualiza en función de los datos de los sensores, lo que le permite reaccionar a obstáculos en tiempo real y ajustar su ruta.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/88da9e3c-4542-41d4-a2f8-ddcd1c8df03b)



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
| Montreal  | Failed | Muere en la chican|
| Nürburgring|  268 |  268 |

Circuito simple -> 135s
Montmelo -> 
Montreal ->
Nürburgring ->

### Objetivo cumplido ‼️​

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/d26031de-3822-4127-af6b-03fe0f97fb87)




