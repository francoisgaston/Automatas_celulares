import pandas as pd
import matplotlib.pyplot as plt
import glob

# Directorio donde se encuentran los archivos CSV
directory = "../Simulation/Automatas/output/extra/"

# Encuentra todos los archivos CSV que coinciden con el patrón
files = glob.glob(directory + "Polarization_100_*.csv")

# Leer y combinar todos los archivos CSV
dfs = []
for file in files:
    dfs.append(pd.read_csv(file))
df = pd.concat(dfs)

# Grafica el counter en función del tiempo, separado por noise
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'y', 'k', 'y', 'y']
noise_values = df['Noise'].unique()

for idx, noise in enumerate(noise_values):
    data = df[df['Noise'] == noise]
    plt.scatter(data['tiempo'], data['polarization'], c=colors[idx], label=f"Noise {noise}")

plt.xlabel('Tiempo')
plt.ylabel('polarization')
plt.title('polarization vs Tiempo')
plt.legend()
plt.show()

