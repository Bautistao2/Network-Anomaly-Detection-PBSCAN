import os
import requests
import gzip
import shutil
import pandas as pd

# 📌 URLs del dataset KDD99
URL_DATA = "https://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz"
URL_NAMES = "https://kdd.ics.uci.edu/databases/kddcup99/kddcup.names"

# 📂 Directorios
DATA_DIR = os.path.abspath("data/")
RAW_FILE_GZ = os.path.join(DATA_DIR, "kddcup.data_10_percent.gz")
RAW_FILE = os.path.join(DATA_DIR, "kddcup.data_10_percent")
CSV_FILE = os.path.join(DATA_DIR, "kddcup_data.csv")

# 📌 Crear carpeta "data" si no existe
if not os.path.exists(DATA_DIR):
    print("📂 Creando carpeta data/")
    os.makedirs(DATA_DIR, exist_ok=True)
else:
    print("✅ Carpeta data/ ya existe")

# 🔽 Paso 1: Descargar los archivos
def download_file(url, output_file):
    if os.path.exists(output_file):
        print(f"✅ Archivo ya descargado: {output_file}")
        return
    
    print(f"🔽 Descargando {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print(f"✅ Descarga completa: {output_file}")
    else:
        print(f"❌ ERROR: No se pudo descargar {url}. Código {response.status_code}")

# 🗜️ Paso 2: Descomprimir el archivo .gz
def decompress_gz(input_file, output_file):
    if os.path.exists(output_file):
        print(f"✅ Archivo ya descomprimido: {output_file}")
        return
    
    print("🗜️ Descomprimiendo archivo...")
    if os.path.exists(input_file):
        with gzip.open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"✅ Archivo descomprimido: {output_file}")
    else:
        print(f"❌ ERROR: No se encontró {input_file}")

# 📊 Paso 3: Convertir a CSV con nombres de columnas
def convert_to_csv(input_file, output_csv):
    print("📊 Procesando datos y convirtiendo a CSV...")

    columns = [
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
        "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
        "logged_in", "num_compromised", "root_shell", "su_attempted",
        "num_root", "num_file_creations", "num_shells", "num_access_files",
        "num_outbound_cmds", "is_host_login", "is_guest_login",
        "count", "srv_count", "serror_rate", "srv_serror_rate",
        "rerror_rate", "srv_rerror_rate", "same_srv_rate",
        "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
        "dst_host_srv_count", "dst_host_same_srv_rate",
        "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
        "dst_host_srv_serror_rate", "dst_host_rerror_rate",
        "dst_host_srv_rerror_rate", "label"
    ]

    if os.path.exists(input_file):
        df = pd.read_csv(input_file, header=None, names=columns)
        df.to_csv(output_csv, index=False)
        print(f"✅ Datos guardados en {output_csv}")
    else:
        print(f"❌ ERROR: No se encontró {input_file}")

# 🛠️ Paso 4: Ejecutar el pipeline completo
if __name__ == "__main__":
    print("🚀 Iniciando proceso de descarga y conversión...")

    # 1. Descargar los archivos
    download_file(URL_DATA, RAW_FILE_GZ)
    download_file(URL_NAMES, os.path.join(DATA_DIR, "kddcup.names"))

    # 2. Descomprimir el dataset
    decompress_gz(RAW_FILE_GZ, RAW_FILE)

    # 3. Convertir a CSV
    convert_to_csv(RAW_FILE, CSV_FILE)

    # 4. Eliminar archivos temporales (opcional)
    if os.path.exists(RAW_FILE): os.remove(RAW_FILE)
    if os.path.exists(RAW_FILE_GZ): os.remove(RAW_FILE_GZ)
    print("🗑️ Archivos temporales eliminados.")
