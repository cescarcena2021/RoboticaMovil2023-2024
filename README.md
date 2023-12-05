# Global Navigation 🏎️

## Objetivo 🎯
El objetivo de esta práctica es implementar la lógica de un algoritmo de Gradient Path Planning (GPP). La navegación global a través de GPP consta de:

* Seleccionado un destino, el algoritmo de GPP es responsable de encontrar la ruta más corta hacia él, evitando, en el caso de esta práctica, todo lo que no sea carretera.
* Una vez seleccionada la ruta, se debe implementar la lógica necesaria para seguir esta ruta y alcanzar el objetivo en el robot.

## Gradient Path Planning
Para esta práctica, usaremos una técnica de navegación global conocida como Gradient Path Planning. La idea detrás de esta técnica es crear un mapa dividido en celdas a la cuales se les asignara un peso en funcion de lo lejos o de lo cerca que esten del coche. De esta forma consegimos un gradiente parecido al de la imagen, siendo el pinto mas alto el coche, y el pinto mas bajo el objetivo

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/d12ba1b4-56cc-4fb9-83d8-cd307dbe7556)

Pero a esto hay que añadirle un complicacion, ya que en la vida real, el mundo no es plano. Existen multidud de obtaculos que un coche no puede atrabesar, y es lo que pasa en este caso con las paredes del mapa. Estas paredes necesitan  tener un coste muy grande en el gradiente para evitar que el coche las atraviese. De tal forma que el gradiente que ya teniamos, mas el reajuste de costes a las paredes, deberia quedar algo asi:

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/0b64c1c4-d7ff-4cbf-8928-75cb07185fd9)

## Obtencion del camino
Parsaber por donde tenemos que ir es muy sencillo una vez tenemos el gradiente, ya que simplemente hay que escoger el camino mas corto posible. En este caso se puede ver como el camino claramente es la linea verde.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/ae50a680-49a0-4284-8d03-a9927b7cbc66)


## Navegación

Una vez ya tenemos el path la navegacion es realivamente sencilla. La tecnica que he usado a sido ir recorriendo el path punto por punto para ir de uno a otro, es decir, voy del punto A al punto B y cuando ya estoy en B voy al C y asi sucesibamente hasta llegar al objetivio. Para ir de un punto a otro, primero me he centrado en la orientacion. 

* **Orientacion**: Para abrodar el tema de la orientacion he usado la arcontangente que relaciona el angulo del coche respecto del siguiente punto. Y una vez sabiendo ese error, simplemete se va corrigiendo poco a poco hasta que este error sea practicamete inexistente. Cuando estatmos perfectamenete alineados con el punto ya podemos ir hacia el.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/1f2d3a39-d89c-4d8b-af96-75f9da00afb9)

* **Distancia**: para saber la distanca tambien he usado una teorema metematico y es el caso del teorema de pitragoras. Con este teorema posdemos sacar los conocidos como catetos que son la diferencia en x y en y de los puntos, para posterirmente obtener la hipotenusa, que en este caso es la distancia entre puntos. Con esto ya somos capaces de saber la distancia a la que estamos, y si hemos alcanzado el objetivo. En caso que alcancemos el objetivo, iremos a por el siguiente.

![image](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/95134e4e-b381-4fda-8726-2ccec6aa7c34)


## Demostración

[Screencast from 12-05-2023 09:02:56 PM.webm](https://github.com/cescarcena2021/RoboticaMovil2023-2024/assets/102520602/102d6ba1-21a8-4548-b4cd-e60d66f37102)




  





