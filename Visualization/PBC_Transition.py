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
N = 1500
L = 5
RADIUS = 0.5
N_CIRCLES = 4
TIMES = 4000
BREAK = 75
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

def save_plot_data(parcial_count, noises):
    with open('output/Circles_PBC_' + str(BREAK*100/N) + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['Noise','Tiempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        plt.figure(figsize=(10, 6))
        cmap = plt.get_cmap('tab10')
        num_colors = len(parcial_count)
        colors = [cmap(i) for i in np.linspace(0, 1, num_colors)]
        
        for index_file,file_vector in enumerate(parcial_count):
            for index_circle, circle_vector in enumerate(file_vector):
                acumulado = 0
                ready = True
                array_acumulado = []
                for index, valor in enumerate(circle_vector):
                    acumulado += valor
                    array_acumulado.append(acumulado/N)
                    if acumulado >= (BREAK/100)*N and ready:
                        ready = False
                        writer.writerow({'Noise': noises[index_file], 'Tiempo': index})
                if noises[index_file] == '0.0' or noises[index_file] == '2.0' or noises[index_file] == '4.0':
                    if index_circle == 0:
                        plt.plot(array_acumulado, label=f'Ruido = {noises[index_file]}', color=colors[index_file])
                    else:
                        plt.plot(array_acumulado, color=colors[index_file])
        
        plt.axhline(y=BREAK/100, color='red', linestyle='--', linewidth=2)

        print("---------------------------------------")
        print("Datos guardados en: " + "output/Circles_PBC_" + str(BREAK) + '.csv')

        plt.xlabel('Tiempo[s]', fontsize=16)
        plt.ylabel('Porcentaje de Particulas', fontsize=16)
        plt.legend(bbox_to_anchor=(0.5, 1.15), loc='upper center', borderaxespad=0, fontsize=12, ncol=3)
        plt.show()


def main():

    circles = generate_circles()
    noises = []
    parcial_count = []

    parcial_count, noises = read_files(parcial_count, noises, circles)

    save_plot_data(parcial_count, noises)


if __name__ == "__main__":
    main()

