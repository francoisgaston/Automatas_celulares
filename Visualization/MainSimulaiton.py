import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import imageio.v2 as imageio

PARTICLES_COORDINATES_FILE = ''
CONFIG_FILE = '../TP1/input.json'
CIM_NEIGHBOURS_FILE = '../TP1/cim_output.json'


# Leer el archivo CSV
df = pd.read_csv('../Simulation/Automatas/output/DataSimulation.csv')

# Obtener valores únicos de tiempo
tiempos = df['time'].unique()

# Definir el radio del círculo para representar la partícula
radio_particula = 2

# Iterar sobre los tiempos
for tiempo in tiempos:
    # Filtrar los datos para el tiempo actual
    datos_tiempo = df[df['time'] == tiempo]
    
    # Crear una nueva figura
    plt.figure()
    
    # Graficar la posición de la partícula
    plt.scatter(datos_tiempo['x'], datos_tiempo['y'], color='blue')
    
    # Graficar la velocidad y el ángulo como flechas
    for index, fila in datos_tiempo.iterrows():
        dx = np.cos(fila['angulo']) * fila['vel']
        dy = np.sin(fila['angulo']) * fila['vel']
        plt.arrow(fila['x'], fila['y'], dx, dy, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # Configurar los ejes
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xlabel('Posición X')
    plt.ylabel('Posición Y')
    plt.title(f'Gráfico de simulación - Tiempo {tiempo}')
    
    # Dibujar círculos para representar las partículas
    for index, fila in datos_tiempo.iterrows():
        circulo = plt.Circle((fila['x'], fila['y']), radio_particula, color='red', fill=False)
        plt.gca().add_artist(circulo)
    
    # Guardar la figura como un archivo PNG
    plt.savefig(f'img/plot_tiempo_{tiempo}.png')
    
    # Cerrar la figura para liberar memoria
    plt.close()

# Directorio donde se encuentran las imágenes PNG
directorio_imagenes = './img/'

# Obtener la lista de archivos PNG en el directorio
archivos_png = [f for f in os.listdir(directorio_imagenes) if f.endswith('.png')]

# Ordenar los archivos PNG en base a los tiempos
archivos_png.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))

# Lista para almacenar las imágenes a unir
imagenes = []

# Leer cada archivo PNG y agregarlo a la lista de imágenes
for archivo in archivos_png:
    ruta_imagen = os.path.join(directorio_imagenes, archivo)
    imagenes.append(imageio.imread(ruta_imagen))

# Ruta de salida para el archivo GIF
ruta_gif = './output.gif'

# Escribir las imágenes en un archivo GIF
imageio.mimsave(ruta_gif, imagenes, duration=1000)  # Duración de cada imagen en segundos
