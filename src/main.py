import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.distancia import optimal_eps 

# Asegurar que Python encuentre el directorio raíz del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_preprocessing import load_and_preprocess_data
from src.clustering import pbscan_clustering, prepare_data_for_pbscan  
from src.anomaly_detection import visualize_anomalies

if __name__ == "__main__":
    print("\U0001F680 Iniciando Análisis de Tráfico con PBSCAN...")

    # Preparar datos con PCA
    data_pca = prepare_data_for_pbscan("../data/kddcup_data.csv", sample_size=10000, n_components=8)

    # Visualizar la distribución de PCA_1 y PCA_8 antes de DBSCAN
    plt.figure(figsize=(10, 5))
    plt.scatter(data_pca["PCA_1"], data_pca["PCA_8"], s=5, alpha=0.5)
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 8")
    plt.title("Distribución de los datos después de PCA")
    plt.grid()
    plt.show()

    # Incrementar `eps` un 10%
    optimal_eps *= 1.1  
    print(f"🔹 Usando eps aumentado en 10%: {optimal_eps:.4f}")

    # Aplicar PBSCAN
    labels, anomalies = pbscan_clustering(data_pca, eps=optimal_eps)
    print(f"🔹 Anomalías detectadas: {len(anomalies)}")

    # Verificar si se detectaron anomalías antes de visualizarlas
    if len(anomalies) > 0:
        # Visualizar anomalías detectadas sin filtros
        plt.figure(figsize=(10, 5))
        plt.scatter(data_pca["PCA_1"], data_pca["PCA_8"], s=5, alpha=0.3, label="Datos normales")
        plt.scatter(data_pca.iloc[anomalies]["PCA_1"], data_pca.iloc[anomalies]["PCA_8"], 
                    s=10, alpha=0.8, color='red', label="Anomalías")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 8")
        plt.title("Distribución de Anomalías en PCA")
        plt.legend()
        plt.grid()
        plt.show()
    else:
        print("⚠️ No se detectaron anomalías en los datos.")
    
    visualize_anomalies(data_pca, labels, anomalies)
    print("✅ Análisis completado.")

    # Cargar los datos originales para mapear anomalías
    print("📊 Cargando datos originales para mapear anomalías...")
    data_original = load_and_preprocess_data("../data/kddcup_data.csv")

    # Verificar que `anomalies` tiene los índices correctos
    if isinstance(anomalies, np.ndarray):
        anomalies = anomalies.tolist()

    # Extraer las anomalías del dataset original
    original_anomalies = data_original.iloc[anomalies]

    # Guardar las anomalías en un archivo CSV para análisis posterior
    anomalies_file = "../data/anomalies.csv"
    original_anomalies.to_csv(anomalies_file, index=False)
    print(f"✅ Anomalías guardadas en {anomalies_file} para análisis posterior.")
