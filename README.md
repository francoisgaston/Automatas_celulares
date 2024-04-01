# Automatas celulares - Off Lattice #

Repositorio correspondiente al segundo trabajo practico de la materia Simulacion de sistemas - 72.25 en el cual se simula y analiza el comportamiento de un sistema Off Lattice.

## Ejecución

### Simulación y visualización
Para realizar una simulación revisar que el archvio **_Simulation/Automatas/input/input.json_** contenga los valores que desea introducir en la simulación

````json
{
  "noise": "Ruido que se quiera introducir al sisitema"
  "L": "Largo y ancho de la simulación"
  "speed": "Velocidad de las particulas"
  "N": "Numero de particulas en la simulación"
  "interactionRadius": "Radio de interacción de cada particula"
  "CircleBoundaryConditions": "Las particulas poseen nuevo Id en caso de salir a los margenes"
  "totalTime": "Tiempo total de la simulación"
}
````
Una vez establecidos estos valores correr la función main del codigo java, el cual generará un archivo **_SimulationData_N_L_Noise.csv_** con los datos dinamicos de la simulación y un archivo **_StateData_N_L_Noise.csv_** con los datos de estado de la simulación.

Si se desea visualizar la animación dirigirse a la carpeta visualization y correr el comando

````bash
python3 MainSimulation.py
````

### Analisis de Polaridad - Ruido

Para realizar este analisis se provee la función **_NoiseMultiSimulation()_** dentro del condigo java. Esta función correrá todas las simulaciones necesarias para el posterior analisis.

Una vez realizadas las simulaciones necesarias dirigirse a la carpeta visualization y correr el comando

````bash
python3 Noise_Transicion.py
````
Este script mostrará la evolución de la polarización en el tiempo y dado un tiempo establecido (en caso de querer cambiarlo revisar el final de la sección) devolverá en el archivo **_Noise_N_L.csv_** los valores de polarización promedios y desviacion standart estacionarios para cada ruido. Si se desea ver la evolución de la polarización en funcion del ruido correr el comando

````bash
python3 Noise_Va.py
````

si se desea modificar algún input de la simulación, dirigirse al archivo **_Simulation/Automatas/input/Noiseinput.json_** y modificar los valores como se explicó en la sección "Simulación y visualización". A continuación dirigirse a **_Noise_Transicion.py_** y modificar los valores constates con los mismos valores deseados.

### Analisis de Polaridad - Densidad

Para realizar este analisis se provee la función **_DensityMultiSimulation()_** dentro del condigo java. Esta función correrá todas las simulaciones necesarias para el posterior analisis.

Una vez realizadas las simulaciones necesarias dirigirse a la carpeta visualization y correr el comando

````bash
python3 Density_Transicion.py
````
Este script mostrará la evolución de la polarización en el tiempo y dado un tiempo establecido (en caso de querer cambiarlo revisar el final de la sección) devolverá en el archivo **_Density_L_Noise.csv_** los valores de polarización promedios y desviacion standart estacionarios para cada densidad. Si se desea ver la evolución de la polarización en funcion de la densidad correr el comando

````bash
python3 Density_Va.py
````

Si se desea modificar algún input de la simulación, dirigirse al archivo **_Simulation/Automatas/input/Densityinput.json_** y modificar los valores como se explicó en la sección "Simulación y visualización". A continuación dirigirse a **_Density_Transicion.py_** y modificar los valores constates con los mismos valores deseados.

### Analisis de zonas de conteo (PBC)

Antes de comenzar con este analisis dirigirse al archivo **_Simulation/Automatas/input/CircleNoiseinput.json_** y revisar que el campo **_CircleBoundaryConditions esté en false_**.

Para realizar este analisis se provee la función **_CircleNoiseMultiSimulation()_** dentro del condigo java. Esta función correrá todas las simulaciones necesarias para el posterior analisis.

Una vez realizadas las simulaciones necesarias dirigirse a la carpeta visualization y correr el comando

````bash
python3 PBC_Transicion.py
````
Este script mostrará la evolución del porcentaje de particulas en el tiempo y dado un porcentaje establecido (en caso de querer cambiarlo revisar el final de la sección) devolverá en el archivo **_Circles_PBC_Porcentaje.csv_** los valores del tiempo en alcanzar tal porcentaje para cada zona para cada tiempo. Si se desea ver la evolución del tiempo en función del ruido correr el comando

````bash
python3 PBC_Noise.py
````

Si se desea modificar algún input de la simulación, dirigirse al archivo **_Simulation/Automatas/input/CircleNoiseinput.json_** y modificar los valores como se explicó en la sección "Simulación y visualización". A continuación dirigirse a **_PBC_Transicion.py_** y modificar los valores constates con los mismos valores deseados.

### Analisis de zonas de conteo (OBC)

Antes de comenzar con este analisis dirigirse al archivo **_Simulation/Automatas/input/CircleNoiseinput.json_** y revisar que el campo **_CircleBoundaryConditions esté en true_**.

Para realizar este analisis se provee la función **_CircleNoiseMultiSimulation()_** dentro del condigo java. Esta función correrá todas las simulaciones necesarias para el posterior analisis.

Una vez realizadas las simulaciones necesarias dirigirse a la carpeta visualization y correr el comando

````bash
python3 OBC_Transicion.py
````
Este script mostrará la evolución de la cantidad de particulas en el tiempo y calculará el valor de pendiente adecuado para cada curva en el archivo **_Circles_OBC.csv_**. Si se desea ver la evolución de la pendiente en función del ruido correr el comando

````bash
python3 OBC_Noise.py
````

Si se desea modificar algún input de la simulación, dirigirse al archivo **_Simulation/Automatas/input/CircleNoiseinput.json_** y modificar los valores como se explicó en la sección "Simulación y visualización". A continuación dirigirse a **_OBC_Transicion.py_** y modificar los valores constates con los mismos valores deseados.


## Requerimientos

### Python Packages ###
1. pandas
2. matplotlib
3. numpy
4. opencv-python

### Visualization Options ###
1. python MainVisualization.py normal
    - Runs Off-Lattice automaton with four circles placed around (randomly).
2. python MainVisualization.py gray
    - Runs Off-Lattice automaton with gray-scale colored particles which change colors according to velocity angle.
3. python MainVisualization.py rainbow
    - Runs Off-Lattice automaton with gray-scale colored particles which change colors according to velocity angle.
4. python MainVisualization.py
    - Runs Off-Lattice automaton in normal mode.

## Autores

- 62500 - [Gastón Ariel Francois](https://github.com/francoisgaston)
- 62655 - [Andres Carro Wetsel](https://github.com/AndresCarro)
