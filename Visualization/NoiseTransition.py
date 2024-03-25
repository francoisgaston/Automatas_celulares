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
AVG_PATH = './output/'
N = 401
L = 10
T_ESTACIONARIO = 400
# ---------------------------------------------------

def custom_palette_with_skip(skip_color, polarized_df):
    palette = sns.color_palette("husl", len(polarized_df['noise'].unique()))
    new_palette = [color for color in palette if color != sns.color_palette()[skip_color]]
    return new_palette

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

def merge_all_files():
    # Obtener lista de archivos en los directorios
    csv_files = os.listdir(OUTPUT_PATH)
    filter_start = 'SimulationData_' + str(N) + "_" + str(L)
    filter_end =  '.csv'

    # Combinar archivos uno a uno
    combined_data = pd.DataFrame()
    for csv_file in csv_files:
        if csv_file.endswith(filter_end) and csv_file.startswith(filter_start):
            print("Procesando: " + csv_file)
            csv_path = os.path.join(OUTPUT_PATH, csv_file)
            json_path = csv_path.replace("SimulationData_", "StateData_").replace(".csv", ".json")
            df = merge_csv_and_json(csv_path, json_path)
            combined_data = pd.concat([combined_data, df], ignore_index=True)
    
    return combined_data


def calculate_polarization(combined_df):
    # Calcula las componentes x e y de las velocidades
    combined_df['vel_x'] = combined_df['vel'] * np.cos(combined_df['angulo'])
    combined_df['vel_y'] = combined_df['vel'] * np.sin(combined_df['angulo'])

    # Agrupar por noise y luego por time
    grouped = combined_df.groupby(['noise', 'time'])

    # Calcular la suma de vel_x y vel_y para cada grupo de tiempo
    sum_velocities = grouped[['vel_x', 'vel_y']].sum()
    result = grouped.first()[['vel', 'boundary', 'totalTime', 'L', 'radius', 'N', 'speed']]

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

def plot_transition(polarized_df, tiempo_X):
    # Definir colores personalizados para los diferentes niveles de ruido
    custom_palette = custom_palette_with_skip(1, polarized_df)

    sns.lineplot(data=polarized_df, x="time", y="resultado", hue="noise", palette=custom_palette)

    # Agregar una línea vertical roja en el tiempo 200
    plt.axvline(x=tiempo_X, color='red', linestyle='--', linewidth=2)

    # Añadir título y etiquetas de ejes
    plt.title('Resultado vs Tiempo por Nivel de Ruido')
    plt.xlabel('Tiempo')
    plt.ylabel('Resultado')

    # Mostrar la gráfica
    plt.show()

def save_final(polarized_df, tiempo_X):
    # Filtrar el DataFrame para los tiempos mayores o iguales a X
    df_tiempo_X = polarized_df[polarized_df['time'] >= tiempo_X]

    # Calcular el promedio y la desviación estándar de los resultados agrupados por el nivel de ruido
    resultados_agrupados = df_tiempo_X.groupby('noise')['resultado']
    for noise_data in resultados_agrupados:
        index = 0
        total_value = 0
        for value in noise_data:
            print(value)
            index += 1
            total_value += value
        total_value /= index
        print("PROMEDIO" + str(total_value))

    
    promedio_resultados = resultados_agrupados.mean()
    desviacion_estandar_resultados = resultados_agrupados.std()

    # Escribir los datos en un archivo CSV
    promedio_desviacion_df = pd.DataFrame({'Noise': promedio_resultados.index, 'Promedio_Resultado': promedio_resultados, 'Desviacion_Estandar': desviacion_estandar_resultados})
    promedio_desviacion_df.to_csv(AVG_PATH + 'Noise_' + str(N) + "_" + str(L) + '.csv', index=False)
    print("---------------------------------------")
    print("Datos guardados en: " + AVG_PATH + 'Noise_' + str(N) + "_" + str(L) + '.csv')


def main():
    # Combinar todos los archivos CSV y JSON
    combined_df = merge_all_files()

    # Calcular la polarización
    polarized_df = calculate_polarization(combined_df)

    # Definir el tiempo de corte
    tiempo_X = T_ESTACIONARIO

    # Graficar la transición de los resultados
    plot_transition(polarized_df, tiempo_X)

    # Graficar y guardar el promedio y la desviación estándar de los resultados para tiempos mayores o iguales a X
    save_final(polarized_df, tiempo_X)


if __name__ == "__main__":
    main()

