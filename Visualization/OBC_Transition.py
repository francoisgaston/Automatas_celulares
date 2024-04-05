import os
import pandas as pd
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import matplotlib.pyplot as plt
import csv
import re


# ---------------------------------------------------
# DATOS A CAMBIAR SEGÚN EL CASO DE ESTUDIO
# ---------------------------------------------------
OUTPUT_PATH = '../Simulation/Automatas/output/'
N = 600
L = 5
RADIUS = 0.5
N_CIRCLES = 4
TIMES = 4000
STEPS = 5
# ---------------------------------------------------


class Circle:
    def __init__(self, L, radius):
        self.x = random.uniform(0, L)
        self.y = random.uniform(0, L)
        self.radius = radius
        self.particles_set = set()

    def add_point(self, id):
        self.particles_set.add(id)
    
    def cointains_id(self, id):
        return id in self.particles_set
    
    def inside_circle(self, x, y):
        return (x - self.x)**2 + (y - self.y)**2 <= self.radius**2

    def clear_set(self):
        self.particles_set = set()

def generate_circles():
    circles = [Circle(L, RADIUS) for _ in range(N_CIRCLES)]
    print("---------------------------------------")
    print("Circulos generados:")
    for circle in circles:
        print("x: " + str(circle.x) + ", Y: " + str(circle.y) + "radio: " + str(circle.radius))
    print("---------------------------------------")
    return circles

def read_files(parcial_count, noises, circles):
    index_files = -1
    csv_files = os.listdir(OUTPUT_PATH)
    filter_start = 'SimulationData_' + str(N) + "_" + str(L)
    filter_end =  '.csv'
    for csv_file in csv_files:
        if csv_file.endswith(filter_end) and csv_file.startswith(filter_start):
            print("Procesando: " + csv_file)
            index_files += 1

            noises.append(re.search(r'(\d+(\.\d+)?)\.csv', csv_file).group(1))

            parcial_count.append([[0 for _ in range(TIMES)], [0 for _ in range(TIMES)], [0 for _ in range(TIMES)], [0 for _ in range(TIMES)]])

            df = pd.read_csv(OUTPUT_PATH + csv_file) 

            next(df.iterrows(), None)

            for circle in circles:
                circle.clear_set()

            for index, row in df.iterrows():
                x = float(row['x'])
                y = float(row['y'])
                id = int(row['id'])
                time = int(row['time'])

                for index_circle, circle in enumerate(circles):
                    if circle.inside_circle(x, y) and not circle.cointains_id(id):
                        circle.add_point(id)
                        parcial_count[index_files][index_circle][time] += 1
    
    return parcial_count, noises

def plot_data(parcial_count, noises):
    plt.figure(figsize=(10, 6))
    cmap = plt.get_cmap('tab10')
    num_colors = len(parcial_count)
    colors = [cmap(i) for i in np.linspace(0, 1, num_colors)]
    
    for index_file,file_vector in enumerate(parcial_count):
        for index_circle, circle_vector in enumerate(file_vector):
            acumulado = 0
            array_acumulado = []
            for valor in circle_vector:
                acumulado += valor
                array_acumulado.append(acumulado)
            if noises[index_file] == '0.0' or noises[index_file] == '2.0' or noises[index_file] == '4.0':
                if index_circle == 0:
                    plt.plot(array_acumulado, label=f'Ruido {noises[index_file]}', color=colors[index_file])
                else:
                    plt.plot(array_acumulado, color=colors[index_file])
    
    print("---------------------------------------")
    print("Datos guardados en: output/Circles_PBC.csv")

    plt.xlabel('Tiempo[s]', fontsize=16)
    plt.ylabel('Numero de particulas', fontsize=16)
    plt.legend(bbox_to_anchor=(0.5, 1.15), loc='upper center', borderaxespad=0, fontsize=12, ncol=3)
    plt.show()


def prom_data(parcial_count):
    prom_count = []
    for index_file, file_vector in enumerate(parcial_count):
        prom_count.append([])
        aux = 0
        for index_valor in range(TIMES):
            for index_circle in range(N_CIRCLES):
                aux += parcial_count[index_file][index_circle][index_valor]
            prom_count[index_file].append(aux/N_CIRCLES)
    return prom_count


def save_best_c(prom_count, noises):
    best_c = []
    with open('output/Circles_OBC.csv', 'w', newline='') as csvfile:
        fieldnames = ['Noise','Pendiente','Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for index_file, file_vector in enumerate(prom_count):
            error = 0.005
            plot = (noises[index_file] == '2.0')
            c = best_c_alg(file_vector, error, plot)
            writer.writerow({'Noise': noises[index_file], 'Pendiente': c, 'Error':error})
            best_c.append(c)
    return best_c

def best_c_alg(values, apreciacion, plot):

    init_c = 0
    max_c = 1
    plt.figure(figsize=(10, 6))
    min_error = float('inf')
    best_c = 0
    step = int(max_c / apreciacion)

    for step_index in range(step):
        c = init_c + step_index * apreciacion
        error = 0
        for index_value, value in enumerate(values):
            error += (value - c*index_value) ** 2
        if plot:
            plt.scatter(c, error, color='red', s=10)
        if error < min_error:
            min_error = error
            best_c = c
    if plot:
        plt.axvline(x=best_c, color='green', linestyle='--', linewidth=2)

        plt.xlabel('Pendiente', fontsize=16)
        plt.ylabel('Error', fontsize=16)
        plt.show()
    return best_c

def regresion_best_c(values):

    init_c = 0
    max_c = 2
    grid = 100
    prev_error = (TIMES*N) ** 2

    for times in range(STEPS):
        grid_division_value = init_c
        for step in range(grid):
            error = 0
            for index_value, value in enumerate(values):
                error += (value - grid_division_value*index_value) ** 2
            if error > prev_error:
                break
            else:
                prev_error = error
            grid_division_value += (max_c-init_c)/grid
        
        init_c = grid_division_value - (max_c-init_c)/grid - (max_c-init_c)/grid
        if init_c < 0:
            init_c = 0
        max_c = grid_division_value
    
    return max_c, prev_error

def linea_recta(x, m):
    return m * x

def main():

    circles = generate_circles()
    noises = []
    parcial_count = []

    parcial_count, noises = read_files(parcial_count, noises, circles)

    plot_data(parcial_count, noises)

    prom_count = []

    prom_count = prom_data(parcial_count)

    best_c = save_best_c(prom_count, noises)

    plt.figure(figsize=(10, 6))

    for prom in prom_count:
        plt.plot(prom)

    for c in best_c:
        x = range(0, TIMES)
        y = [linea_recta(xi, c) for xi in x] 
        plt.plot(x, y)

    plt.xlabel('Numero de particulas', fontsize=16)
    plt.ylabel('Tiempo[s]', fontsize=16)
    plt.show()
    


if __name__ == "__main__":
    main()

