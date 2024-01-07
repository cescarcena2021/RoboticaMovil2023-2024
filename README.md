# Monte Carlo Laser Localization

## Objetivo 🎯
El objetivo de esta práctica es localizar un robot asperjador en una casa. Para ello, se pide que creemos un algoritmo de localización basado en un filtro de partículas que se van reubicando en función de la ubicación del robot.

## Implementación
Para la implementación, he seguido los siguientes pasos:

- Creación de las partículas
- Propagación de partículas
- Cálculo de pesos
- Resampleo de las partículas
- Actualizar y volver a empezar

### Generación de partículas 📍​
Para la generación de partículas, lo primero que hice fue crear un punto aleatorio que tuviera 3 coordenadas: la x, la y y la dirección a la que está apuntando. Además de eso, esta partícula tenía que estar ubicada aleatoriamente dentro de los límites del mapa. Estos pasos se repiten por cada partícula que quieras lanzar. Sin embargo, hay un problema, ya que algunas partículas podrían caer en obstáculos y no tendría sentido. Para solucionar esto, en un primer instante decidí no tener en cuenta las que caían en obstáculos, pero pronto me di cuenta de que si la mayoría caía en obstáculos, no tendría partículas útiles. Por lo tanto, se me ocurrió que a la hora de inicializar las partículas, si caían en obstáculos, se generarían de nuevo hasta que cayeran en un sitio correcto. De esta forma, conseguimos que siempre se generen el número esperado de partículas con seguridad.

### Obtención de pesos ⚖️
Una vez que todas las partículas están aleatoriamente ubicadas, es el turno de saber cuáles son las más adecuadas. Para ello, por cada partícula, obtenemos las medidas que nos ofrece el láser y las comparamos con las medidas obtenidas en el láser del robot. Comparamos cada punto del láser virtual del robot con cada punto del láser virtual de la partícula y obtenemos el error o distancia que hay entre ellos. Una vez que tenemos el error de todos los puntos, hacemos una media de todos ellos y obtenemos el error de la partícula respecto al robot. Una vez que tenemos el error, calcular el peso es fácil, ya que el peso es inversamente proporcional al error, es decir, cuanto más error, menos peso y viceversa.

### Movimiento, resampleo y propagación
Cuando ya tenemos los pesos, es el turno de reubicar las partículas peor posicionadas. Para ello, usamos las funciones ya proporcionadas. Y para el movimiento del robot y de las partículas, también usamos las funciones ya proporcionadas.

## Optimizaciones ⚙️​🔧​
Todo este proceso es computacionalmente pesado y además, Python solo nos permite usar un hilo de nuestro procesador. Por ello, he realizado algunas de las optimizaciones propuestas en clase. La primera de ellas fue reducir el mapa de 1024 píxeles a 400 píxeles, reduciendo notablemente el tiempo de cómputo. La segunda optimización fue reducir la cantidad de medidas del láser, es decir, en lugar de verificar las 180 medidas del láser de las N partículas, simplemente comprobamos 1 de cada diez medidas, reduciendo las medidas de cada partícula de 180 a 18 sin perder demasiada precisión para el algoritmo.

## Demostración 📹​
[Screencast from 01-07-2024 07:29:48 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/99432f42-e0ef-4bc1-b355-3ccc887669c0)
[Screencast from 01-07-2024 10:40:24 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/ed2cbb27-a07d-4f90-a3a6-98051045d0d4)

[Screencast from 01-07-2024 10:40:50 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/f77997aa-810d-4fbf-ace1-8ee9bab2194c)
[Screencast from 01-07-2024 10:42:14 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/1b7d5a33-d8f8-4645-a9df-a67d3f041f91)
