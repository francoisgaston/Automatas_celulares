import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv("../Simulation/Automatas/output/DataPolarization.csv")

# Extraer los datos de tiempo y polarización
tiempo = df['tiempo']
polarization = df['polarization']

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(tiempo, polarization, marker='o', linestyle='-')
plt.title('Gráfico de Polarización en Función del Tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Polarización')
plt.grid(True)
plt.show()