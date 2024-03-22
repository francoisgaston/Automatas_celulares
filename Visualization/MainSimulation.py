import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sys
import cv2
from matplotlib.animation import FFMpegWriter

PARTICLES_COORDINATES_FILE = '../Simulation/Automatas/output/DataSimulation.csv'
CIRCLES_COORDINATES_FILE = '../Simulation/Automatas/output/DataCircles.csv'
CONFIG_FILE = '../Simulation/Automatas/input/input.json'
CIM_NEIGHBOURS_FILE = '../TP1/cim_output.json'
IMG_DIR = './img/'
OPENCV_OUTPUT_FILENAME = 'output/open_cv_output'
MATPLOTLIB_OUTPUT_FILENAME = 'output/matplotlib_output'
BACKGROUND_FILE = '/img/white_image.jpeg'
GIF_FORMAT = 'gif'
MP4_FORMAT = 'mp4'
WIDTH, HEIGHT = 640, 480
SCALE_FACTOR = 50
ANGLE_TO_RGB = 255 / (np.pi*2)
NORMAL_MODE = 'normal'
RAINBOW_MODE = 'rainbow'
GRAY_MODE = 'gray'


def angle_to_rgb(angle, mode):
    base_value = 100
    color_coefficient = 0.4
    if mode == GRAY_MODE:
        red = color_coefficient * (angle * ANGLE_TO_RGB) + base_value
        green = color_coefficient * (angle * ANGLE_TO_RGB) + base_value
        blue = color_coefficient * (angle * ANGLE_TO_RGB) + base_value
    elif mode == RAINBOW_MODE:
        red = np.clip(255 * np.abs(np.sin(angle)), 0, 255)
        green = np.clip(255 * np.abs(np.sin(angle + np.pi)), 0, 255)
        blue = np.clip(255 * np.abs(np.cos(angle + np.pi)), 0, 255)
    else:
        red = 0
        green = 0
        blue = 255

    return int(blue), int(green), int(red)


def complete_visualization_matplotlib(particles_coords, timeFrames, particle_radius, L, amount_circles, circle_radius, circle_coords):
    writer = FFMpegWriter(fps=5)

    figure = plt.figure()

    with writer.saving(figure, MATPLOTLIB_OUTPUT_FILENAME + '.' + MP4_FORMAT, 1000):
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

            for index, fila in circle_coords.iterrows():
                if index > amount_circles:
                    break
                circulo = plt.Circle((fila['x'], fila['y']), circle_radius, color='green', fill=False)
                plt.gca().add_artist(circulo)

            writer.grab_frame()
            # Clear figure
            plt.clf()


def complete_visualization_opencv(particles_coords, timeFrames, particle_radius, L, amount_circles, circle_radius, circle_coords, mode):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(OPENCV_OUTPUT_FILENAME + '.' + MP4_FORMAT, fourcc, 10.0, (L*SCALE_FACTOR, L*SCALE_FACTOR))
    for timeFrame in timeFrames:
        current_particle_coords = particles_coords[particles_coords['time'] == timeFrame]
        frame = np.zeros((L*SCALE_FACTOR, L*SCALE_FACTOR, 3), dtype=np.uint8)

        for index, fila in current_particle_coords.iterrows():
            dx = np.cos(fila['angulo']) * fila['vel'] * SCALE_FACTOR
            dy = np.sin(fila['angulo']) * fila['vel'] * SCALE_FACTOR
            start_pos = [int(fila['x'] * SCALE_FACTOR), int(fila['y'] * SCALE_FACTOR)]
            finish_pos = [int(SCALE_FACTOR * fila['x']) + int(dx), int(SCALE_FACTOR * fila['y']) + int(dy)]
            cv2.arrowedLine(frame, tuple(start_pos), tuple(finish_pos), (angle_to_rgb(fila['angulo'], mode)), 5, cv2.LINE_AA)
            current_pos = [int(fila['x'] * SCALE_FACTOR), int(fila['y'] * SCALE_FACTOR)]
            cv2.circle(frame, tuple(current_pos), particle_radius * SCALE_FACTOR, (angle_to_rgb(fila['angulo'], mode)), -1)

        if mode == NORMAL_MODE:
            for index, fila in circle_coords.iterrows():
                if index > amount_circles:
                    break
                current_pos = [int(fila['x'] * SCALE_FACTOR), int(fila['y'] * SCALE_FACTOR)]
                cv2.circle(frame, tuple(current_pos), circle_radius * SCALE_FACTOR, (0, 255, 0), 5)

        video_writer.write(frame)
    video_writer.release()
    cv2.destroyAllWindows()


def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


def delete_images():
    for file_name in os.listdir(IMG_DIR):
        file_path = os.path.join(IMG_DIR, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def parse_console_command(argv):
    if len(argv) == 1 or argv[1] == NORMAL_MODE:
        return NORMAL_MODE
    elif argv[1] == RAINBOW_MODE:
        return RAINBOW_MODE
    else:
        return GRAY_MODE


if __name__ == '__main__':
    config = read_config_file(CONFIG_FILE)
    particles_coords = pd.read_csv(PARTICLES_COORDINATES_FILE)
    circle_coords = pd.read_csv(CIRCLES_COORDINATES_FILE)
    timeFrames = particles_coords['time'].unique()
    particle_radius = config['interactionRadius']
    visualization_mode = parse_console_command(sys.argv)

    # OpenCV #
    print('Drawing particles with opencv...')
    complete_visualization_opencv(particles_coords, timeFrames, particle_radius, config['L'], config['NCircles'],
                           config['RCircles'], circle_coords, visualization_mode)
    print('DONE!')

    # Matplotlib #
    #print('Drawing particles with matplotlib...')
    #complete_visualization_matplotlib(particles_coords, timeFrames, particle_radius, config['L'], config['NCircles'],
                           #config['RCircles'], circle_coords)
    #print('DONE!')
