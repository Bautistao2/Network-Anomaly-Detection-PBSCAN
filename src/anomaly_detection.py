import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def visualize_anomalies(data, labels, anomalies):
    """
    Visualiza los clusters y las anomalías detectadas.
    """
    print("📊 Generando visualización de anomalías...")

    # Asegurar que data es un DataFrame con nombres de columnas correctos
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data, columns=[f"PCA_{i+1}" for i in range(data.shape[1])])

    # Crear copia del DataFrame para evitar modificar el original
    data_viz = data.copy()
    data_viz["Cluster"] = labels

    # Crear directorio de resultados si no existe
    results_dir = "../results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Crear gráfico de dispersión con PCA
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="PCA_1", y="PCA_8", hue="Cluster", palette="tab10", alpha=0.6, data=data_viz)

    # Resaltar anomalías en rojo con borde negro para mejor visibilidad
    if len(anomalies) > 0:
        anomaly_data = data_viz.iloc[anomalies]
        plt.scatter(anomaly_data["PCA_1"], anomaly_data["PCA_8"], 
                    color='red', edgecolor='black', linewidth=1, marker="x", label="Anomalías", s=80)
    
    plt.legend()
    plt.title("Clusters y Anomalías Detectadas con PBSCAN")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 8")
    plt.grid()
    
    # Guardar automáticamente la gráfica
    save_path = os.path.join(results_dir, "anomalies_visualization.png")
    plt.savefig(save_path, dpi=300)
    plt.show()
    print(f"✅ Visualización completada y guardada en '{save_path}'.")
