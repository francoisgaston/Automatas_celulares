import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import imageio.v2 as imageio
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter

PARTICLES_COORDINATES_FILE = '../Simulation/Automatas/output/DataSimulation.csv'
CONFIG_FILE = '../Simulation/Automatas/input/input.json'
CIM_NEIGHBOURS_FILE = '../TP1/cim_output.json'
IMG_DIR = './img/'
OUTPUT_FILENAME = 'output/output'
GIF_FORMAT = 'gif'
MP4_FORMAT = 'mp4'


def draw_moving_particles(particles_coords, timeFrames, particle_radius, L, output_format):
    if output_format not in ['mp4', 'gif']:
        raise ValueError('Invalid output format. Please choose mp4 or gif')

    if output_format == 'gif':
        writer = PillowWriter(fps=5)
    else:
        writer = FFMpegWriter(fps=5)

    figure = plt.figure()

    with writer.saving(figure, OUTPUT_FILENAME + '.' + output_format, 1000):
        for timeFrame in timeFrames:
            current_particle_coords = particles_coords[particles_coords['time'] == timeFrame]
            plt.scatter(current_particle_coords['x'], current_particle_coords['y'], color='blue')

            for index, fila in current_particle_coords.iterrows():
                dx = np.cos(fila['angulo']) * fila['vel']
                dy = np.sin(fila['angulo']) * fila['vel']
                plt.arrow(fila['x'], fila['y'], dx, dy, head_width=0.2, head_length=0.2, fc='black', ec='black')

            plt.xlim(0, L)
            plt.ylim(0, L)
            plt.xlabel('Posición X')
            plt.ylabel('Posición Y')
            plt.title(f'Gráfico de simulación - Tiempo {timeFrame}')

            for index, fila in current_particle_coords.iterrows():
                circulo = plt.Circle((fila['x'], fila['y']), particle_radius, color='red', fill=False)
                plt.gca().add_artist(circulo)

            writer.grab_frame()
            # Clear figure
            plt.clf()


def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


def delete_images():
    for file_name in os.listdir(IMG_DIR):
        file_path = os.path.join(IMG_DIR, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


if __name__ == '__main__':
    config = read_config_file(CONFIG_FILE)
    particles_coords = pd.read_csv(PARTICLES_COORDINATES_FILE)
    timeFrames = particles_coords['time'].unique()
    particle_radius = config['interactionRadius']
    draw_moving_particles(particles_coords, timeFrames, particle_radius, config['L'], MP4_FORMAT)
