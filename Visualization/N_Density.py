import os
import pandas as pd
import matplotlib.pyplot as plt

# Directorio donde se encuentran los archivos CSV
directorio = './avg/'

# Lista para almacenar los datos combinados
datos_combinados = []

# Iterar sobre cada archivo CSV en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith('.csv'):
        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(os.path.join(directorio, archivo))
        # Agregar una columna para el nombre del archivo para distinguir los datos
        df['Archivo'] = os.path.splitext(archivo)[0]
        # Agregar los datos ala lista
        datos_combinados.append(df)

# Combinar todos los DataFrames en uno solo
datos_combinados = pd.concat(datos_combinados, ignore_index=True)

# Graficar
plt.figure(figsize=(10, 6))

for nombre_archivo, datos in datos_combinados.groupby('Archivo'):
    plt.errorbar(datos['Noise'], datos['Promedio_Resultado'], yerr=datos['Desviacion_Estandar'], fmt='o', label=nombre_archivo)

plt.xlabel('Ruido')
plt.ylabel('Polarización Promedio')
plt.title('Polarización Promedio vs Ruido')
plt.legend()
plt.grid(True)
plt.show()
