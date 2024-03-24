import os
import pandas as pd
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import matplotlib.pyplot as plt


# ---------------------------------------------------
# DATOS A CAMBIAR SEGÚN EL CASO DE ESTUDIO
# ---------------------------------------------------
OUTPUT_PATH = '../Simulation/Automatas/output/'
N = 300
L = 5
RADIUS = 1
N_CIRCLES = 4
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

def valores_acumulativos(array):
    acumulado = 0
    array_acumulado = []
    for valor in array:
        acumulado += valor
        array_acumulado.append(acumulado)
    return array_acumulado



def main():
    # Obtener lista de archivos en los directorios
    csv_files = os.listdir(OUTPUT_PATH)
    filter_start = 'SimulationData_' + str(N) + "_" + str(L)
    filter_end =  '.csv'
    
    circles = [Circle(L, RADIUS) for _ in range(N_CIRCLES)]
    parcial_count = []
    for circle in circles:
        print(circle.x, circle.y, circle.radius)

    index_files = -1
    for csv_file in csv_files:
        if csv_file.endswith(filter_end) and csv_file.startswith(filter_start):
            index_files += 1
            print("Procesando: " + csv_file)

            parcial_count.append([[0 for _ in range(1000)], [0 for _ in range(1000)], [0 for _ in range(1000)], [0 for _ in range(1000)]])

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


    final_count = []
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for index,file_vector in enumerate(parcial_count):
        for circle_vector in file_vector:
            plt.plot(valores_acumulativos(circle_vector), color=colors[index])
    
    for i, vector in enumerate(final_count):
        plt.plot(vector, label=f'Vector {i+1}')

    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Gráfica de los 24 vectores')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

