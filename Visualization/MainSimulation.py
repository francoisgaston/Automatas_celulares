import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import imageio.v2 as imageio

PARTICLES_COORDINATES_FILE = '../Simulation/Automatas/output/DataSimulation.csv'
CONFIG_FILE = '../Simulation/Automatas/input/input.json'
CIM_NEIGHBOURS_FILE = '../TP1/cim_output.json'
IMG_DIR = './img/'
GIF_FILENAME = './output.gif'

def write_output_gif(particles_coords, timeFrames, particle_radius):
    for tiempo in timeFrames:
        # Filtrar los datos para el tiempo actual
        datos_tiempo = particles_coords[particles_coords['time'] == tiempo]

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
            circulo = plt.Circle((fila['x'], fila['y']), particle_radius, color='red', fill=False)
            plt.gca().add_artist(circulo)

        # Guardar la figura como un archivo PNG
        plt.savefig(f'img/plot_tiempo_{tiempo}.png')

        # Cerrar la figura para liberar memoria
        plt.close()

        # Obtener la lista de archivos PNG en el directorio
        archivos_png = [f for f in os.listdir(IMG_DIR) if f.endswith('.png')]

        # Ordenar los archivos PNG en base a los tiempos
        archivos_png.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))

        # Lista para almacenar las imágenes a unir
        imagenes = []

        # Leer cada archivo PNG y agregarlo a la lista de imágenes
        for archivo in archivos_png:
            ruta_imagen = os.path.join(IMG_DIR, archivo)
            imagenes.append(imageio.imread(ruta_imagen))

        # Escribir las imágenes en un archivo GIF
        imageio.mimsave(GIF_FILENAME, imagenes, duration=1000)  # Duración de cada imagen en segundos


def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


if __name__ == '__main__':
    config = read_config_file(CONFIG_FILE)
    particles_coords = pd.read_csv(PARTICLES_COORDINATES_FILE)
    timeFrames = particles_coords['time'].unique()
    particle_radius = config['interactionRadius']
    write_output_gif(particles_coords, timeFrames, particle_radius)