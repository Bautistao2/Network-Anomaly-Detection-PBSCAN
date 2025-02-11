import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🛠️ Asegurar que src/ está en el path

results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))

from src.data_preprocessing import load_and_preprocess_data

# 📊 Crear directorio de resultados si no existe
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# 📊 Cargar los datos originales y anomalías
data = load_and_preprocess_data("../data/kddcup_data.csv")

# 📌 Archivo con anomalías detectadas
anomalies_file = "../data/anomalies.csv"
if not os.path.exists(anomalies_file) or os.stat(anomalies_file).st_size == 0:
    print("❌ ERROR: No se encontró el archivo de anomalías o está vacío. Ejecuta primero `python -m src.main`.")
    sys.exit(1)

original_anomalies = pd.read_csv(anomalies_file)
print(f"📊 {len(original_anomalies)} anomalías cargadas desde {anomalies_file}")

# 📊 Comparación de estadísticas clave
stats_data = data.describe()
stats_anomalies = original_anomalies.describe()
comparison = pd.concat([stats_data, stats_anomalies], axis=1, keys=["Datos Normales", "Anomalías"])
print("\n📊 Comparación de estadísticas entre datos normales y anomalías:")
print(comparison)

# 🔍 Identificar variables con mayor diferencia
diff = (stats_anomalies.loc["mean"] - stats_data.loc["mean"]).abs()
top_differences = diff.sort_values(ascending=False).head(min(5, len(diff)))

if len(top_differences) < 2:
    print("❌ ERROR: No hay suficientes diferencias significativas entre anomalías y datos normales.")
    sys.exit(1)

print("\n🔹 Variables con mayor diferencia entre anomalías y datos normales:")
print(top_differences)

# 📊 📈 1️⃣ Matriz de Correlación de Variables Clave
plt.figure(figsize=(10, 8))
sns.heatmap(original_anomalies[top_differences.index].corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("🔍 Matriz de Correlación en Anomalías")
plt.savefig(os.path.join(results_dir, "matriz_correlacion_anomalias.png"), dpi=300)
plt.show()

# 📊 📉 2️⃣ Scatter Plots de Variables Clave
for i in range(len(top_differences.index) - 1):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data[top_differences.index[i]], y=data[top_differences.index[i + 1]], alpha=0.3, label="Datos Normales")
    sns.scatterplot(x=original_anomalies[top_differences.index[i]], y=original_anomalies[top_differences.index[i + 1]], color="red", alpha=0.7, label="Anomalías")
    plt.xlabel(top_differences.index[i])
    plt.ylabel(top_differences.index[i + 1])
    plt.legend()
    plt.title(f"Comparación de {top_differences.index[i]} vs {top_differences.index[i+1]}")
    plt.grid()
    plt.savefig(os.path.join(results_dir, f"scatter_{top_differences.index[i]}_vs_{top_differences.index[i+1]}.png"), dpi=300)
    plt.show()

# 📊 🔥 3️⃣ Heatmap de Frecuencia de Anomalías en Variables Clave
plt.figure(figsize=(10, 6))
sns.kdeplot(data=original_anomalies, x=top_differences.index[0], y=top_differences.index[1], cmap="Reds", fill=True, warn_singular=False)
plt.xlabel(top_differences.index[0])
plt.ylabel(top_differences.index[1])
plt.title("🔥 Densidad de Anomalías en Variables Más Relevantes")
plt.savefig(os.path.join(results_dir, "densidad_anomalias.png"), dpi=300)
plt.show()


print("✅ Análisis de anomalías completado. Imágenes guardadas en la carpeta 'results'.")
