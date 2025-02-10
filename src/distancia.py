import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import IncrementalPCA
from sklearn.neighbors import NearestNeighbors
import sys
import os

# 🛠️ Asegurar que src/ está en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_preprocessing import load_and_preprocess_data  # Importamos la función correcta

# 📊 Cargar y preprocesar datos
print("📊 Cargando y preprocesando los datos...")
data = load_and_preprocess_data("../data/kddcup_data.csv")

# 🔹 Usar solo una muestra de 50,000 filas para acelerar el cálculo
sample_size = min(50000, len(data))
data_sample = data.sample(n=sample_size, random_state=42)

# 🔍 Aplicar PCA en lotes para optimizar memoria
print("🔍 Aplicando PCA en lotes...")
pca = IncrementalPCA(n_components=1, batch_size=10000)
data_pca = pca.fit_transform(data_sample)

# 📏 Calcular distancias con NearestNeighbors
print("📏 Calculando distancias con NearestNeighbors...")
neighbors = NearestNeighbors(n_neighbors=5, algorithm="ball_tree", n_jobs=-1)
neighbors_fit = neighbors.fit(data_pca)
distances, _ = neighbors_fit.kneighbors(data_pca)

# 🔢 Ordenar distancias del 4to vecino más cercano
distances = np.sort(distances[:, 4], axis=0)

# 🔹 Calcular eps basado en la mediana y desviación estándar
median_eps = np.median(distances)
std_eps = np.std(distances)
optimal_eps = median_eps + (0.5 * std_eps)  # Ajuste del 50% de la variabilidad

print(f"🔹 Valor recomendado para eps (mediana + 0.5*σ): {optimal_eps:.4f}")

# 📈 Graficar la curva de distancias
plt.figure(figsize=(8, 5))
plt.plot(distances)
plt.axhline(y=optimal_eps, color='r', linestyle='--', label=f"eps óptimo ({optimal_eps:.4f})")
plt.xlabel("Puntos ordenados")
plt.ylabel("Distancia al 4to vecino más cercano")
plt.title("Curva para seleccionar 'eps'")
plt.legend()
plt.grid()
plt.show()

print("✅ Proceso completado.")