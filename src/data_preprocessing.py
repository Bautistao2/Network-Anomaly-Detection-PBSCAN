import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

def load_and_preprocess_data(csv_file):
    """Loads the dataset, selects relevant columns, and correctly normalizes the data."""
    print("📊 Loading data...")
    df = pd.read_csv(csv_file)

    # 🔹 Select only relevant numerical columns for PBSCAN
    selected_features = [
        "duration", "src_bytes", "dst_bytes", "wrong_fragment",
        "count", "srv_count", "serror_rate", "srv_serror_rate",
        "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
        "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate"
    ]

    df = df[selected_features]

    # 🔹 Normalize the data using RobustScaler
    print("⚙️ Correctly normalizing data...")
    scaler = RobustScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=selected_features)

    # 🔹 Verify values after normalization
    print("📊 Summary of normalized data:")
    print(df_scaled.describe())

    return df_scaled

if __name__ == "__main__":
    data = load_and_preprocess_data("../data/kddcup_data.csv")
    print("✅ Preprocessing complete. Data ready for PBSCAN.")
