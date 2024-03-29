import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sys
import cv2
from matplotlib.animation import FFMpegWriter


# ---------------------------------------------------
# DATOS A CAMBIAR SEGÚN EL CASO DE ESTUDIO
# ---------------------------------------------------
OUTPUT_PATH = '../Simulation/Automatas/output/'
AVG_PATH = './output/'
L = 10
NOISE = 0.0
N = 400
RADIUS_CIRCLES = 1
# ---------------------------------------------------

PARTICLES_COORDINATES_FILE2 = ('../Simulation/Automatas/output/SimulationData_' + str(N) + '_' + str(L) + '_' +
                               str(NOISE) + '.csv')
CIRCLES_COORDINATES_FILE = '../Simulation/Automatas/output/Circles_' + str(N) + '_' + str(NOISE) + '.csv'
CONFIG_FILE = '../Simulation/Automatas/input/input.json'
OPENCV_OUTPUT_FILENAME = 'output/open_cv_output'
MATPLOTLIB_OUTPUT_FILENAME = 'output/matplotlib_output'
MP4_FORMAT = 'mp4'
SCALE_FACTOR = 150
ANGLE_TO_RGB = 255 / (np.pi*2)

# ---------------------------------------------------
# Input de comandos
# ---------------------------------------------------
NORMAL_MODE = 'normal'
RAINBOW_MODE = 'rainbow'
GRAY_MODE = 'gray'
FILL = 'fill'
NO_FILL = 'nofill'
# ---------------------------------------------------


def angle_to_rgb(angle, mode, circle_coords, circle_radius, particle_pos, amount_circles):
    base_value = 100
    color_coefficient = 0.4
    blue, green, red = 0,0,0
    if mode == GRAY_MODE:
        red = color_coefficient * (angle * ANGLE_TO_RGB) + base_value
        green = color_coefficient * (angle * ANGLE_TO_RGB) + base_value
        blue = color_coefficient * (angle * ANGLE_TO_RGB) + base_value
    elif mode == RAINBOW_MODE:
        red = (255 * np.abs(np.cos(angle))) % 255
        green = (255 * np.abs(np.sin(angle + np.pi))) % 255
        blue = (255 * np.abs(np.cosh(angle))) % 255
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


def complete_visualization_opencv(particles_coords, timeFrames, particle_radius, L, amount_circles, circle_radius,
                                  circle_coords, mode, fill_mode):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(OPENCV_OUTPUT_FILENAME + '.' + MP4_FORMAT, fourcc, 15.0, (L*SCALE_FACTOR,
                                                                                             L*SCALE_FACTOR))
    for timeFrame in timeFrames:
        current_particle_coords = particles_coords[particles_coords['time'] == timeFrame]
        frame = np.full((L*SCALE_FACTOR, L*SCALE_FACTOR, 3), 255, dtype=np.uint8)

        for index, fila in current_particle_coords.iterrows():
            dx = np.cos(fila['angulo']) * fila['vel'] * SCALE_FACTOR
            dy = np.sin(fila['angulo']) * fila['vel'] * SCALE_FACTOR
            start_pos = [int(fila['x'] * SCALE_FACTOR), int(fila['y'] * SCALE_FACTOR)]
            finish_pos = [int(SCALE_FACTOR * fila['x']) + int(dx), int(SCALE_FACTOR * fila['y']) + int(dy)]
            current_pos = [int(fila['x'] * SCALE_FACTOR), int(fila['y'] * SCALE_FACTOR)]
            cv2.arrowedLine(frame, tuple(start_pos), tuple(finish_pos),
                            (angle_to_rgb(fila['angulo'], mode, circle_coords, circle_radius, current_pos, amount_circles)),
                            5, cv2.LINE_AA)
            if fill_mode == NO_FILL:
                cv2.circle(frame, tuple(current_pos), int(particle_radius * SCALE_FACTOR),
                           (angle_to_rgb(fila['angulo'], mode, circle_coords, circle_radius, current_pos, amount_circles)), 0)
            else:
                cv2.circle(frame, tuple(current_pos), int(particle_radius * SCALE_FACTOR),
                           (angle_to_rgb(fila['angulo'], mode, circle_coords, circle_radius, current_pos, amount_circles)), -1)

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


def parse_console_command(argv):
    if FILL in argv:
        fill_mode = FILL
    else:
        fill_mode = NO_FILL

    if NORMAL_MODE in argv:
        return NORMAL_MODE, fill_mode
    elif RAINBOW_MODE in argv:
        return RAINBOW_MODE, fill_mode
    else:
        return GRAY_MODE, fill_mode


if __name__ == '__main__':
    config = read_config_file(OUTPUT_PATH + 'StateData_' + str(N) + '_' + str(L) + '_' + str(NOISE) + '.json')
    particles_coords = pd.read_csv(PARTICLES_COORDINATES_FILE2)
    #circle_coords = pd.read_csv(CIRCLES_COORDINATES_FILE)
    circle_coords = [
        {'x': 4.359879568940831, 'y': 4.359879568940831, 'id': 0},
        {'x': 5.401094653149744, 'y': 8.884408555473165, 'id': 1},
        {'x': 7.219434561125443, 'y': 0.23352880823145794, 'id': 2}
    ]
    timeFrames = particles_coords['time'].unique()
    particle_radius = config['radius']
    visualization_mode, fill_mode = parse_console_command(sys.argv)

    # OpenCV #
    print('Drawing particles with opencv...')
    complete_visualization_opencv(particles_coords, timeFrames, particle_radius, L, N,
                           RADIUS_CIRCLES, circle_coords, visualization_mode, fill_mode)
    print('DONE!')

    # Matplotlib #
    #print('Drawing particles with matplotlib...')
    #complete_visualization_matplotlib(particles_coords, timeFrames, particle_radius, config['L'], config['NCircles'],
                           #config['RCircles'], circle_coords)
    #print('DONE!')
