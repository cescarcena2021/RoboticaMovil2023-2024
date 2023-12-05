# Global Navigation 🏎️

# Objetivo 🎯
El objetivo de esta práctica es implementar la lógica de un algoritmo de Gradient Path Planning (GPP). La navegación global a través de GPP consta de:

Seleccionado un destino, el algoritmo de GPP es responsable de encontrar la ruta más corta hacia él, evitando, en el caso de esta práctica, todo lo que no sea carretera.
Una vez seleccionada la ruta, se debe implementar la lógica necesaria para seguir esta ruta y alcanzar el objetivo en el robot.

# Gradient Path Planning ⚜️​
Para esta práctica, usaremos una técnica de navegación global conocida como Gradient Path Planning. La idea detrás de esta técnica es crear un mapa dividido en celdas a las cuales se les asignará un peso en función de lo lejos o de lo cerca que estén del coche. De esta forma conseguimos un gradiente parecido al de la imagen, siendo el punto más alto el coche, y el punto más bajo el objetivo.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/d12ba1b4-56cc-4fb9-83d8-cd307dbe7556)

Pero a esto hay que añadirle una complicación, ya que en la vida real, el mundo no es plano. Existen multitud de obstáculos que un coche no puede atravesar, y es lo que pasa en este caso con las paredes del mapa. Estas paredes necesitan tener un coste muy grande en el gradiente para evitar que el coche las atraviese. De tal forma que el gradiente que ya teníamos, más el reajuste de costes a las paredes, debería quedar algo así:

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/0b64c1c4-d7ff-4cbf-8928-75cb07185fd9)

## Algoritmo de búsqueda 🔍
Como algoritmo de búsqueda en este caso, he usado A* (A estrella), que es uno de los más potentes junto a Dijkstra. Lo que hace mi algoritmo es:

* Inicialización:
El bucle while priority_queue: indica que continuará hasta que la cola de prioridad esté vacía.
cost, current = heapq.heappop(priority_queue): Extrae el nodo con el menor costo actual de la cola de prioridad.

* Condición de Finalizacion:
if current == start: break: Si el nodo actual es el nodo de inicio, se rompe el bucle, indicando que se ha encontrado la ruta.

* Manejo de Nodos Visitados:
if visited[current]: continue: Si el nodo actual ya ha sido visitado, se ignora y se pasa al siguiente.

* Actualización de Nodos Visitados:
visited[current] = True: Marca el nodo actual como visitado.

* Obtención de Vecinos:
vecinos = get_neighbors(current, map): Obtiene los nodos vecinos del nodo actual.

* Iteración sobre Vecinos:
Se itera sobre cada vecino y se realiza lo siguiente:
Si el vecino es un obstáculo, se asigna un mayor costo (obstacle_weight = 255), de lo contrario, el costo es 1.
Si el vecino no ha sido visitado antes, se calcula el costo total hasta ese vecino y se agrega a la cola de prioridad con el nuevo costo.

Además, se actualiza el mapa de costos (cost_map) asignando el nodo actual como el padre del vecino.


```python
#Vamos iternado para sacar el costmap
while priority_queue:
    cost, current = heapq.heappop(priority_queue)

    if current == start:
        break

    if visited[current]:
        continue

    visited[current] = True

    #Obtenemos los vecinos para seguir expandiendo
    vecinos = get_neighbors(current, map)

    for vecino in vecinos:

        #Si es un obstaculo se le da un mayor coste     
        if vecino in obstacle_set:
            obstacle_weight = 255  
        else:
            obstacle_weight = 1

        #Y finalmente si no ha sido visitado antes, se añade a el costmap
        if not visited[vecino]:

            cost_to_neighbor = obstacle_weight + cost

            heapq.heappush(priority_queue, (cost_to_neighbor, vecino))
            cost_map[vecino] = current
```

Para la obtención de los vecinos, he reciclado una función que hemos utilizado en la asignatura de Inteligencia Artificial. Esta función toma las posibles direcciones en las que puede ir el coche y las añade a una lista como vecinos. Tuve que agregar un if para el caso de las casillas en los extremos, ya que estas no podían tener vecinos en una dirección, al estar al borde del mapa. El uso de esto es muy similar al de Inteligencia Artificial, ya que en este caso buscamos los vecinos de un taxi, mientras que en el caso de IA eran las posibles siguientes casillas para Pacman.

```python
def get_neighbors(current, map):

    vecinos = []
    x, y = current

    filas, columnas = map.shape

    #Lista con las direciones posibles
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in movimientos:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < filas and 0 <= new_y < columnas:
            vecinos.append((new_x, new_y))

    return vecinos
```

## Obtención del camino 👌​
Para saber por dónde tenemos que ir, es muy sencillo una vez tenemos el gradiente, ya que simplemente hay que escoger el camino más corto posible. En este caso, se puede ver cómo el camino claramente es la línea verde

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/ae50a680-49a0-4284-8d03-a9927b7cbc66)


```python
# En base a el costmap nos da el path correcto
def get_path(start, target, cost_map):
    start = tuple(start)
    target = tuple(target)

    path = []
    current = start

    while current != target:
        path.append(current)
        current = cost_map[current]

    path.append(target)
    return path
```

## Navegación 🛥️​

Una vez que tenemos el camino, la navegación es relativamente sencilla. La técnica que he usado ha sido recorrer el camino punto por punto, es decir, voy del punto A al punto B, y cuando ya estoy en B, voy al C y así sucesivamente hasta llegar al objetivo. Para ir de un punto a otro, primero me he centrado en la orientación.

* **Orientación**: Para abordar el tema de la orientación, he utilizado la arcotangente que relaciona el ángulo del coche respecto al siguiente punto. Y una vez que conocemos ese error, simplemente se va corrigiendo poco a poco hasta que este error sea prácticamente inexistente. Cuando estamos perfectamente alineados con el punto, ya podemos ir hacia él

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/1c9cd2d2-e767-4919-8bbb-28aec2ac7e9c)


```python
def get_angular_error(target_x, target_y):

    current_pose = HAL.getPose3d()
    car_x, car_y = world_to_map(current_pose.x, current_pose.y)

    #Para saber usamos la arcotangente entre el coche y el target
    target_theta = np.arctan2(target_y - car_y, target_x - car_x)
    error = target_theta - current_pose.yaw
    
    #Nos aseguramos que el error esta entre 180 y -180
    if error > math.pi:
        error = -(error - math.pi)
    elif error < -math.pi:
        error = -(error + math.pi)

    return error
```

* **Distancia**: Para determinar la distancia, también he utilizado un teorema matemático, en este caso, el teorema de Pitágoras. Con este teorema, podemos calcular los llamados catetos, que son la diferencia en x y en y de los puntos, para posteriormente obtener la hipotenusa, que en este caso es la distancia entre puntos. Con esto, ya somos capaces de saber la distancia a la que estamos y si hemos alcanzado el objetivo. En caso de que alcancemos el objetivo, iremos a por el siguiente.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/95134e4e-b381-4fda-8726-2ccec6aa7c34)

```python
def get_lineal_error(target_x, target_y):

    current_pose = HAL.getPose3d()
    car_x, car_y = world_to_map(current_pose.x, current_pose.y)

    # En este caso usamos pitagoras para saber la distancia hacia el objetivo
    error = math.sqrt((target_x - car_x)**2 + (target_y - car_y)**2)

    #print("distance_to_local_goal: ", error)

    return error
```

## Problemas ⁉️​

* **Cambio de coordenadas**: Durante la práctica, he dedicado varias horas a entender que el problema, en ocasiones, estaba en el uso incorrecto de las coordenadas. No solo las coordenadas del mapa son distintas a las del mundo, sino que también es necesario invertir las coordenadas del objetivo, ya que la x y la y están intercambiadas. Para imprimir el camino, también he necesitado invertir cada x y cada y del camino para que se "printeara" de forma correcta.

```python
# Invertir las cordenadas del target para pasarlos a cordenadas del mapa
target[0], target[1] = target[1], target[0]

....

# Invertimos las cordenandas
  print_path = [(point[1], point[0]) for point in path]
```

* **Limitación de velocidad**: En esta práctica, o al menos en mi caso, la velocidad a la que el coche alcanza el objetivo es muy lenta. Esto se debe a que tiene que ir de punto a punto todo el tiempo y comprobar continuamente la orientación y la distancia. Esto se ve afectado, ya que cuando llega al punto, hace una pequeña pausa para orientarse. La parte positiva de esto es que es muy robusto y nunca se sale de las líneas, siempre llegando al objetivo.

* **Cercanía a los muros**: Como en cualquier algoritmo de navegación profesional, el robot es tratado como un punto, pero no lo es. Este tiene unas dimensiones dependiendo de cada robot y, si lo tratáramos como un punto sin hacer nada más, rasparía con las paredes e intentaría siempre ir pegado a ellas. Para ello, una buena técnica es engordar los obstáculos. De esta forma, salvamos las distancias entre los límites del coche y las paredes. Por ello, he creado esta función para que reciba la lista de obstáculos y los aumente el factor deseado dependiendo del robot.
  
```python
#Retorna la misma lista que de le proporciona pero con los objetos engordados
def expand_obstacles(obstacle_list, expansion_range, map_shape):

    expanded_obstacles = set()
 
    # Por cada obstaculo del mapa lo engordamos el rango prporcionado
    for obstacle in obstacle_list:
        x, y = obstacle
        for i in range(-expansion_range, expansion_range + 1):
            for j in range(-expansion_range, expansion_range + 1):
                expanded_x, expanded_y = x + i, y + j
 
                # Comprobamos que la expansion no se salga de los limites del mapa y lo añadimos a la lista
                if 0 <= expanded_x < map_shape[0] and 0 <= expanded_y < map_shape[1]:
                    expanded_obstacles.add((expanded_x, expanded_y))
 
    return list(expanded_obstacles)
```

## Demostración 🚕​

[Screencast from 12-05-2023 09:02:56 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/102d6ba1-21a8-4548-b4cd-e60d66f37102)




  





