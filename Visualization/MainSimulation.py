import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import cv2
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter

PARTICLES_COORDINATES_FILE = '../Simulation/Automatas/output/DataSimulation.csv'
CONFIG_FILE = '../Simulation/Automatas/input/input.json'
CIM_NEIGHBOURS_FILE = '../TP1/cim_output.json'
IMG_DIR = './img/'
OUTPUT_FILENAME = 'output/output'
GIF_FORMAT = 'gif'
MP4_FORMAT = 'mp4'
WIDTH, HEIGHT = 640, 480


def visualize_moving_particles(particles_coords, timeFrames, particle_radius, L):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(OUTPUT_FILENAME + '.' + MP4_FORMAT, fourcc, 5.0, (L, L))
    for timeFrame in timeFrames:
        current_particle_coords = particles_coords[particles_coords['time'] == timeFrame]
        frame = np.zeros((L, L, 3), dtype=np.uint8)

        for index, fila in current_particle_coords.iterrows():
            dx = np.cos(fila['angulo']) * fila['vel']
            dy = np.sin(fila['angulo']) * fila['vel']
            start_pos = [int(fila['x']), int(fila['y'])]
            finish_pos = [int(fila['x']) + int(dx), int(fila['y']) + int(dy)]
            cv2.arrowedLine(frame, tuple(start_pos), tuple(finish_pos), (0, 255, 0), 1)
            cv2.circle(frame, tuple(start_pos), particle_radius, (0, 0, 255), 1)

        for index, fila in current_particle_coords.iterrows():
            current_pos = [int(fila['x']), int(fila['y'])]
            cv2.circle(frame, tuple(current_pos), particle_radius//2, (255, 0, 0), -1)

        video_writer.write(frame)
    video_writer.release()
    cv2.destroyAllWindows()


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

    # Matplotlib #
    #draw_moving_particles(particles_coords, timeFrames, particle_radius, config['L'], MP4_FORMAT)

    # OpenCV #
    # L values requires to be > ~500. If lower, video file will be corrupted.
    visualize_moving_particles(particles_coords, timeFrames, particle_radius, config['L'])
