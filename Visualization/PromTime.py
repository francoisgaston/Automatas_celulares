import pandas as pd
import matplotlib.pyplot as plt
import glob
import re

N = 100
L = 10

# Directorio donde se encuentran los archivos CSV
directory = "../Simulation/Automatas/output/extra/"

# Encuentra todos los archivos CSV que coinciden con el patrón
files = glob.glob(directory + "Polarization_*")

pattern = re.compile(r'Polarization(\d+)_(\d+)\.csv')

# Definir el tiempo X
time_X = 0  # Puedes cambiar este valor al tiempo deseado

# Listas para almacenar los datos para el archivo CSV
noise_values_list = []
avg_polarization_list = []
std_polarization_list = []

# Calcular el promedio y la desviación estándar de los valores de polarización después de time_X para cada archivo
for file in files:
    print(file)
    df_file = pd.read_csv(file)
    noise_values = df_file['Noise'].unique()
    for noise in noise_values:
        data = df_file[(df_file['Noise'] == noise) & (df_file['tiempo'] >= time_X)]
        avg_polarization = data['polarization'].mean()
        std_polarization = data['polarization'].std()
        
        noise_values_list.append(noise)
        avg_polarization_list.append(avg_polarization)
        std_polarization_list.append(std_polarization)

# Crear un DataFrame con los valores calculados
df_output = pd.DataFrame({
    'Noise': noise_values_list,
    'Average_Polarization': avg_polarization_list,
    'Std_Polarization': std_polarization_list
})

# Guardar los valores en un archivo CSV
output_csv_file = "./avg/avg" + str(N) + ".csv"
df_output.to_csv(output_csv_file, index=False)

# Graficar el promedio de polarización con barras de error (desviación estándar) en función del ruido
plt.errorbar(noise_values_list, avg_polarization_list, yerr=std_polarization_list, fmt='o')

plt.xlabel('Noise')
plt.ylabel('Average Polarization')
plt.title(f'Average Polarization after Time {time_X}')
plt.show()