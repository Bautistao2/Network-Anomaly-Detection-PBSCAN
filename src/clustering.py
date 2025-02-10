import sys
import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.decomposition import IncrementalPCA
from sklearn.neighbors import KDTree
from src.data_preprocessing import load_and_preprocess_data  # Importar preprocesamiento

# 🛠️ Asegurar que src/ está en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def pbscan_clustering(data, eps, min_samples=None):
    """
    Aplica el algoritmo PBSCAN (DBSCAN mejorado) para la detección de anomalías.
    """
    if min_samples is None:
        min_samples = max(30, int(len(data) * 0.005))  # 0.5% del total de datos
    
    print(f"🧠 Aplicando PBSCAN con eps={eps:.4f} y min_samples={min_samples}...")
    model = DBSCAN(eps=eps, min_samples=min_samples, metric="euclidean", n_jobs=-1)
    labels = model.fit_predict(data)
    
    anomalies = np.where(labels == -1)[0]
    print(f"✅ PBSCAN detectó {len(anomalies)} anomalías en el tráfico de red.")
    
    return labels, anomalies


def prepare_data_for_pbscan(file_path="../data/kddcup_data.csv", sample_size=10000, n_components=8):
    """
    Carga y preprocesa los datos, aplicando PCA antes de pasarlos a PBSCAN.
    """
    print("📊 Cargando y preprocesando datos...")
    data = load_and_preprocess_data(file_path)

    print(f"📊 Tamaño del dataset: {data.shape}")
    if data.shape[0] > sample_size:
        print(f"⚠️ El dataset es muy grande. Seleccionando una muestra de {sample_size} filas...")
        data = data.sample(n=sample_size, random_state=42)

    print(f"🔍 Aplicando PCA con {n_components} componentes...")
    pca = IncrementalPCA(n_components=n_components, batch_size=5000)
    data_pca = pd.DataFrame(pca.fit_transform(data), columns=[f"PCA_{i+1}" for i in range(8)])
    print("✅ PCA aplicado. Nuevas dimensiones:", data_pca.shape)

    return data_pca
