import pandas as pd
import matplotlib.pyplot as plt
import glob

# Directorio donde se encuentran los archivos CSV
directory = "../Simulation/Automatas/output/"

# Encuentra todos los archivos CSV que coinciden con el patrón
files = glob.glob(directory + "Circles_*_*.csv")

# Leer y combinar todos los archivos CSV
dfs = []
for file in files:
    dfs.append(pd.read_csv(file))
df = pd.concat(dfs)

# Grafica el counter en función del tiempo, separado por noise
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
noise_values = df['noise'].unique()

for idx, noise in enumerate(noise_values):
    data = df[df['noise'] == noise]
    plt.scatter(data['tiempo'], data['counter'], c=colors[idx], label=f"Noise {noise}")

plt.xlabel('Tiempo')
plt.ylabel('Counter')
plt.title('Counter vs Tiempo')
plt.legend()
plt.show()