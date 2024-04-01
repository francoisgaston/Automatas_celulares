import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('output/Circles_OBC.csv')

plt.figure(figsize=(10, 6))

for particles, group in df.groupby('Particles'):
    plt.scatter(group['Noise'], group['Pendiente'], label=f'N = {particles}')

plt.xlabel('Ruido[rad]', fontsize=16)
plt.ylabel('Pendiente', fontsize=16)
plt.legend(bbox_to_anchor=(0.5, 1.1), loc='upper center', borderaxespad=0, fontsize=12, ncol=3)
plt.grid(False)
plt.show()