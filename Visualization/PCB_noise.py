import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('output/Circles_PBC_25.0.csv')

# Agrupar por ID y calcular el promedio y la desviación estándar
grouped_data = df.groupby('Noise')['Tiempo'].agg(['mean', 'std'])

# Graficar
plt.figure(figsize=(10, 6))
plt.errorbar(grouped_data.index, grouped_data['mean'], yerr=grouped_data['std'], fmt='o')
plt.xlabel('Ruido[rad]', fontsize=16)
plt.ylabel('Tiempo[s]', fontsize=16)
plt.show()