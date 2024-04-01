import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('output/Circles_PBC_25.0.csv')

plt.figure(figsize=(10, 6))

for particles, group in df.groupby('Particles'):
    # Agrupar por ID y calcular el promedio y la desviación estándar
    grouped_data = group.groupby('Noise')['Tiempo'].agg(['mean', 'std'])
    plt.errorbar(grouped_data.index, grouped_data['mean'], yerr=grouped_data['std'], fmt='o', label=f'N = {particles}')

plt.legend(bbox_to_anchor=(0.5, 1.1), loc='upper center', borderaxespad=0, fontsize=12, ncol=3)
plt.xlabel('Ruido[rad]', fontsize=16)
plt.ylabel('Tiempo[s]', fontsize=16)
plt.show()