# Obstacle Avoidance 🏎️

## Objetivo 🎯
El objetivo de esta práctica es conseguir que nuestro coche de fórmula 1 sea capaz de navegar por la pista, evitando los obstáculos y alcanzando los destinos marcados.

## Navegación VFF
Para esta práctica, usaremos una técnica de navegación conocida como VFF. La idea detrás de esta técnica es crear un mapa local del entorno del robot y utilizarlo para generar un campo de vectores que indique la dirección en la que el robot debe moverse para evitar obstáculos y alcanzar su destino. Aquí tienes un resumen de cómo funciona:

**Mapeo**: El robot utiliza sensores, como cámaras, láseres o ultrasonidos, para recopilar información sobre su entorno inmediato. A partir de estos datos, se construye un mapa local que representa la ubicación de obstáculos, paredes y otros objetos cercanos al robot.

**Generación del campo de vectores**: Se crea un campo de vectores en el que cada punto en el mapa local tiene un vector asociado. Este vector indica la dirección en la que el robot debe moverse desde ese punto para llegar a su destino y evitar obstáculos. Los vectores se generan de manera que el robot sea atraído hacia su objetivo y repelido por los obstáculos.

**Navegación**: El robot sigue los vectores del campo de vectores para navegar de manera autónoma. A medida que el robot se mueve, el campo de vectores se actualiza en función de los datos de los sensores, lo que le permite reaccionar a obstáculos en tiempo real y ajustar su ruta.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/88da9e3c-4542-41d4-a2f8-ddcd1c8df03b)

## Cálculo de fuerzas 🧮💪🏻

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/02db2bb5-cef7-4b46-b700-a22bf3f829d3)

### **Fuerza del objetivo** 🟩
Como hemos comentado antes, para esta técnica es necesario calcular el conjunto de fuerzas. En primer lugar, para calcular el vector de los objetivos, simplemente llamamos a la función **GUI.map.getNextTarget()** y lo modificamos de tal forma que obtenemos su componente x y su componente y. Además de ello, usando la función **absolute2relative** proporcionada en el enunciado, conseguimos obtener las coordenadas del objetivo en forma relativa al coche. Luego simplemente calculamos el vector y lo reducimos en un rango para que no sea muy grande.

```python
# Vector del objetivo en verde
car_vect = [max(min(target_rel_x, 3.5), -3.5), max(min(target_rel_y, 3.2), -3.2)]
```
### Fuerza repulsiva 🟥

Para calcular el vector de repulsión es algo más complejo, puesto que hay que obtener todas las mediciones del láser y calcular la distancia de todas las mediciones para obtener un vector de repulsión resultante. Una vez hemos obtenido todas las mediciones del láser, simplemente hacemos la media de todas ellas para obtener el vector resultante.

```python

# Vector de repulsión en rojo
obs_vect = [get_repulsive_force(laser)[0], get_repulsive_force(laser)[1]]
```
```python

def get_repulsive_force(parse_laser):
    laser = parse_laser

    laser_vectorizado = []
    for dist, angle in laser:

        x = 1/dist * math.cos(angle) * -1
        y = 1/dist * math.sin(angle) * -1

        v = (x, y)
        laser_vectorizado += [v]
    laser_media = np.mean(laser_vectorizado, axis=0)
    return laser_media
```
### Fuerza resultante ⬛

Para calcular la resultante, simplemente hay que sumar las fuerzas en ambas componentes.

```python

# Vector resultante en negro
avg_vector = [(car_vect[0] + obs_vect[0]), (car_vect[1] + obs_vect[1)]
```

## Reparto de fuerzas ⚖️

Para que todo este sistema de navegación funcione, no todas las fuerzas pueden tener la misma importancia. Por ejemplo, como es lógico, la fuerza que atrae a nuestro coche hacia el objetivo tiene que ser mayor. Esto es debido a que si las fuerzas fueran de igual intensidad, el coche sería muy miedoso y rara vez alcanzaría el objetivo. Por otro lado, tampoco hay que exagerar, ya que si esta fuerza no tiene la importancia que debe, el coche será muy poco cuidadoso y en ocasiones chocará con los obstáculos. Por ello, los valores con los que he concluido que el coche no se choca y alcanza los objetivos son:

| Multiplicadores |  Componete X | Componente Y|
| ------------- | ------------- | ------------|
| Vector atración  | x1  |       x1      |
| Vector repulsión  | x3  |    x8         |
| Vector total  | x1 | x0.3 |

Como podemos observar, el vector de atracción es el que no modifico los valores, mientras que sí lo hago en los vectores de repulsión y el total para compensar este primero.
Cómo llegar a los objetivos

Una vez que hemos hecho todos los cálculos de las fuerzas, debemos comandar las velocidades del coche. Para ello, usamos las componentes x e y del vector total. Y para calcular la velocidad lineal, usamos la tangente de la componente x e y.

```python

tan = math.tan(avg_vector[1] / avg_vector[0])
#--------------#
HAL.setW(tan * 2)
HAL.setV(avg_vector[0])
```

## Demostración

Screencast from 11-05-2023 10:37:26 AM.webm
