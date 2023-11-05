# Obstacle Avoidance 🏎️​

## Objetivo 🎯
El objetivo de esta practica es consegir que nuestro coche de formula 1 se capaz de navegar por la pista. Consiguiendio esquivar los obstaculos y alcanzados los destinos marcados.

## Navegacion VFF​
Para esta practica usaremos una tecnica de navegacion conocida como VFF .La idea detrás de est tecnica es crear un mapa local del entorno del robot y utilizarlo para generar un campo de vectores que indica la dirección en la que el robot debe moverse para evitar obstáculos y alcanzar su destino. Aquí hay un resumen de cómo funciona:

**Mapeo**: El robot utiliza sensores, como cámaras, láseres o ultrasonidos, para recopilar información sobre su entorno inmediato. A partir de estos datos, se construye un mapa local que representa la ubicación de obstáculos, paredes y otros objetos cercanos al robot.

**Generación del campo de vectores**: Se crea un campo de vectores en el que cada punto en el mapa local tiene un vector asociado. Este vector indica la dirección en la que el robot debe moverse desde ese punto para llegar a su destino y evitar obstáculos. Los vectores se generan de manera que el robot sea atraído hacia su objetivo y repelido por los obstáculos.

**Navegación**: El robot sigue los vectores del campo de vectores para navegar de manera autónoma. A medida que el robot se mueve, el campo de vectores se actualiza en función de los datos de los sensores, lo que le permite reaccionar a obstáculos en tiempo real y ajustar su ruta.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/88da9e3c-4542-41d4-a2f8-ddcd1c8df03b)


## Calculo de furzas 🧮​💪🏻​

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/02db2bb5-cef7-4b46-b700-a22bf3f829d3)

### **Fuerza del objetivio** 🟩​
Como hemos comentado antes para esta tecnica es necesario calular el conjunto de furzas. En primer lugar, para calcular el vector de los objetivos, simplemete llamamos a la funcion **GUI.map.getNextTarget()** y lo modificmaos de tal forma que obtenemos su componente x y su pomponete y .Ademas de ello usando la funcion **absolute2relative** proporcionada en el enunciado consegiomos obtener las coordenadas del target en forma relativa al coche. Luego simplemente caculamos el vector y lo reducimos en un rango para que este no sea muy grande.
```python3
    # Vector del target en verde
    car_vect = [max(min(target_rel_x, 3.5), -3.5), max(min(target_rel_y, 3.2), -3.2)]
```
### **Fuerza repusiva** ​🟥​
Para calcular el vector repulsion es algo mas complejo, puesto que hay que obtener todas las mediadas del laser y calcualar la distancia de todas las medidas y obtener un vector repulsion resultante. Una vez hemos objetido todas las medidas del laser sumplemente hacemos la media de todas ellas para obtener el vector resultante.
```python3
    # Vector de repulsion en rojo
    obs_vect = [get_repulsive_force(laser)[0], get_repulsive_force(laser)[1]]
```
``` python3
def get_repulsive_force(parse_laser):
    laser = parse_laser
    
    laser_vectorized = []
    for dist, angle in laser:
      
        x = 1/dist * math.cos(angle) * -1
        y = 1/dist * math.sin(angle) * -1

        v = (x,y)
        laser_vectorized += [v]
    laser_mean = np.mean(laser_vectorized, axis=0)
    return laser_mean
```
### **Fuerza resultante** ⬛​
Para caluclar la resultante simplemente hay que hacer la suma de las furzas en ambas componetes

````
# Vector resultante en negro
    avg_vector = [(car_vect[0]+obs_vect[0]), (car_vect[1] + obs_vect[1])]
````

## Reparto de fuerzas ​⚖️
Para que todo este sistema de navegacion funcione, no todas las fuerzas pueden tener la misma importancia. Por ejemplo, como es logico, la fuerza que atrae a nuestro coche al obejetivo. tiene que ser mayor. Esto es debido a que si las fuerzas fueran de igual intensidad, el coche seria muy **miedoso** y rara vez alcanzara el objetivio. Por otro lado tampoco hay que pasarse ya que si esta fuerza ni tienen la importancia que debe, el coche sera muy poco cuidadoso y en ocasiones chocara con los obstaculos. Por ello los valores con los que he concluido que el coche es no se choca y alcanza los objetivos son:

| Multiplicadores |  Componete X | Componente Y|
| ------------- | ------------- | ------------|
| Vector atracion  | x1  |       x1      |
| Vector repulsion  | x3  |    x8         |
| Vector total  | x1 | x0.3 |

Como podemos observar el vector atracion es en el que no modifico los valores mientras que sí lo hago en los vectores de repulsion y total para compensar este primero.







