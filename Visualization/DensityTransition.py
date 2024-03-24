import os
import pandas as pd
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------
# DATOS A CAMBIAR SEGÚN EL CASO DE ESTUDIO
# ---------------------------------------------------
OUTPUT_PATH = '../Simulation/Automatas/output/'
AVG_PATH = './avg/'
L = 20
NOISE = 1.0
# ---------------------------------------------------


def merge_csv_and_json(csv_file, json_file):
    # Leer el JSON
    with open(json_file, 'r') as jf:
        json_data = json.load(jf)
    
    # Leer el CSV y agregar datos del JSON
    df = pd.read_csv(csv_file)
    
    # Añadir los datos del JSON al DataFrame del CSV
    for key, value in json_data.items():
        df[key] = value
    
    return df

def merge_all_files(csv_dir, NOISE, L):
    # Obtener lista de archivos en los directorios
    csv_files = os.listdir(csv_dir)
    filter_start = 'SimulationData_'
    filter_end = str(L) + "_" + str(NOISE) + '.csv'
    
    # Combinar archivos uno a uno
    combined_data = pd.DataFrame()
    for csv_file in csv_files:
        if csv_file.endswith(filter_end) and csv_file.startswith(filter_start):
            print(csv_file)
            csv_path = os.path.join(csv_dir, csv_file)
            json_path = csv_path.replace("SimulationData_", "StateData_").replace(".csv", ".json")
            df = merge_csv_and_json(csv_path, json_path)
            combined_data = pd.concat([combined_data, df], ignore_index=True)
    
    return combined_data

def calculate_polarization(combined_df):
    # Calcula las componentes x e y de las velocidades
    combined_df['vel_x'] = combined_df['vel'] * np.cos(combined_df['angulo'])
    combined_df['vel_y'] = combined_df['vel'] * np.sin(combined_df['angulo'])

    # Agrupar por noise y luego por time
    grouped = combined_df.groupby(['N', 'time'])

    # Calcular la suma de vel_x y vel_y para cada grupo de tiempo
    sum_velocities = grouped[['vel_x', 'vel_y']].sum()

    # También, como mencionaste que algunas columnas van a ser iguales, puedes tomar solo la primera fila de cada grupo
    # Aquí, por ejemplo, estoy tomando solo la primera fila y seleccionando las columnas que no van a cambiar
    result = grouped.first()[['vel', 'boundary', 'totalTime', 'L', 'radius', 'noise', 'speed']]

    # Agregar las sumas de velocidades al DataFrame resultante
    result['suma_vel_x'] = sum_velocities['vel_x']
    result['suma_vel_y'] = sum_velocities['vel_y']

    # Reiniciar el índice si lo deseas
    result = result.reset_index()

    # Calcular la suma vectorial de suma_vel_x y suma_vel_y
    result['suma_vectorial'] = np.sqrt(result['suma_vel_x']**2 + result['suma_vel_y']**2)

    # Dividir la suma vectorial por N y por vel
    result['resultado'] = result['suma_vectorial'] / (result['N'] * result['vel'])

    # Mostrar el resultado
    return result

def plot_transition(polarized_df):
    # Graficar usando seaborn
    sns.set(style="whitegrid")
    sns.lineplot(data=polarized_df, x="time", y="resultado", hue="N", marker='o')

    # Añadir título y etiquetas de ejes
    plt.title('Resultado vs Tiempo por Nivel de Ruido')
    plt.xlabel('Tiempo')
    plt.ylabel('Resultado')

    # Mostrar la gráfica
    plt.show()

def plot_save_final(polarized_df, tiempo_X, NOISE, L):
    # Filtrar el DataFrame para los tiempos mayores o iguales a X
    df_tiempo_X = polarized_df[polarized_df['time'] >= tiempo_X]

    # Calcular el promedio y la desviación estándar de los resultados agrupados por el nivel de ruido
    resultados_agrupados = df_tiempo_X.groupby('N')['resultado']
    promedio_resultados = resultados_agrupados.mean()
    desviacion_estandar_resultados = resultados_agrupados.std()

    # Crear un gráfico de barras
    plt.bar(promedio_resultados.index, promedio_resultados, yerr=desviacion_estandar_resultados, capsize=5)
    plt.xlabel('N')
    plt.ylabel('Promedio de Resultado')
    plt.title('Promedio de Resultado vs. N para time >= {}'.format(tiempo_X))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

    # Escribir los datos en un archivo CSV
    promedio_desviacion_df = pd.DataFrame({'Noise': promedio_resultados.index, 'Promedio_Resultado': promedio_resultados, 'Desviacion_Estandar': desviacion_estandar_resultados})
    promedio_desviacion_df.to_csv(AVG_PATH + 'Density_' + str(L) + "_" + str(NOISE) + '.csv', index=False)


def main():
    # Combinar todos los archivos CSV y JSON
    combined_df = merge_all_files(OUTPUT_PATH, NOISE, L)

    # Calcular la polarización
    polarized_df = calculate_polarization(combined_df)

    print(polarized_df)

    # Graficar la transición de los resultados
    plot_transition(polarized_df)
    
    # Definir el tiempo de corte
    tiempo_X = 2

    # Graficar y guardar el promedio y la desviación estándar de los resultados para tiempos mayores o iguales a X
    plot_save_final(polarized_df, tiempo_X, NOISE, L)


if __name__ == "__main__":
    main()

