import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo CSV
df = pd.read_csv('../Simulation/Automatas/output/DataCircles.csv')

# Agrupar por 'id' y trazar las líneas para cada uno
fig, ax = plt.subplots()
for key, grp in df.groupby(['id']):
    ax.plot(grp['tiempo'], grp['counter'], label=f'ID {key}')

# Etiquetas y título
plt.xlabel('Tiempo')
plt.ylabel('Counter')
plt.title('Counter vs Tiempo para cada ID')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()