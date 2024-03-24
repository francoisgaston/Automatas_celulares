import os
import pandas as pd
import matplotlib.pyplot as plt


def combinar():
    # Lista para almacenar los datos combinados
    datos_combinados = []
    avg_path = './output/'
    filter_start = 'Noise'

    # Iterar sobre cada archivo CSV en el directorio
    for archivo in os.listdir(avg_path):
        if archivo.endswith('.csv') and archivo.startswith(filter_start):
            print("Procesando: " + archivo)
            # Cargar el archivo CSV en un DataFrame
            df = pd.read_csv(os.path.join(avg_path, archivo))
            # Agregar una columna para el nombre del archivo para distinguir los datos
            df['Archivo'] = os.path.splitext(archivo)[0]
            # Agregar los datos ala lista
            datos_combinados.append(df)

    # Combinar todos los DataFrames en uno solo
    datos_combinados = pd.concat(datos_combinados, ignore_index=True)

    return datos_combinados

def plot_final(combined_df):
    # Graficar
    plt.figure(figsize=(10, 6))

    for nombre_archivo, datos in combined_df.groupby('Archivo'):
        plt.errorbar(datos['Noise'], datos['Promedio_Resultado'], yerr=datos['Desviacion_Estandar'], fmt='o', label=nombre_archivo)

    plt.xlabel('Ruido')
    plt.ylabel('Polarización Promedio')
    plt.title('Polarización Promedio vs Ruido')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Unir todos los CSV en un solo DataFrame
    datos_combinados = combinar()

    # Graficar los datos combinados
    plot_final(datos_combinados)


if __name__ == "__main__":
    main()
