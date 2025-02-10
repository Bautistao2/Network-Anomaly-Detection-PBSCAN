import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler

def load_and_preprocess_data(csv_file):
    """
    Carga el dataset, selecciona las columnas relevantes y normaliza los datos eficientemente.
    """
    print("📊 Cargando datos...")
    selected_features = [
        "duration", "src_bytes", "dst_bytes", "wrong_fragment",
        "count", "srv_count", "serror_rate", "srv_serror_rate",
        "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
        "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate"
    ]
    
    df = pd.read_csv(csv_file, usecols=selected_features, dtype={col: "float32" for col in selected_features})

    # Seleccionar el escalador en función de la distribución de los datos
    if df.skew().mean() > 1:
        scaler = RobustScaler()
        print("⚙️ Usando RobustScaler debido a la presencia de valores extremos.")
    else:
        scaler = StandardScaler()
        print("⚙️ Usando StandardScaler para normalización estándar.")

    df[selected_features] = scaler.fit_transform(df)

    print("📊 Resumen de datos normalizados:")
    print(df.describe())
    
    return df

if __name__ == "__main__":
    data = load_and_preprocess_data("../data/kddcup_data.csv")
    print("✅ Preprocesamiento completado. Datos listos para PBSCAN.")
