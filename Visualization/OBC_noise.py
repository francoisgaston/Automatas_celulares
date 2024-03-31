import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('output/Circles_OBC.csv')

# Extraer los datos
noise = df['Noise']
slope = df['Pendiente']
#error = df['Error']

# Crear el gráfico
#plt.errorbar(noise, slope, yerr=error, fmt='o', capsize=5)
plt.figure(figsize=(10, 6))
plt.errorbar(noise, slope, fmt='o', capsize=5)
plt.xlabel('Noise')
plt.ylabel('Pendiente')
plt.title('Gráfico de Noise vs Pendiente con error')
plt.grid(False)
plt.show()