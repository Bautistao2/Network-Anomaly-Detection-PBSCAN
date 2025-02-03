import os
import requests
import gzip
import shutil
import pandas as pd

# 📌 URLs for the KDD99 dataset
URL_DATA = "https://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz"
URL_NAMES = "https://kdd.ics.uci.edu/databases/kddcup99/kddcup.names"

# 📂 Directories
DATA_DIR = os.path.abspath("data/")
RAW_FILE_GZ = os.path.join(DATA_DIR, "kddcup.data_10_percent.gz")
RAW_FILE = os.path.join(DATA_DIR, "kddcup.data_10_percent")
CSV_FILE = os.path.join(DATA_DIR, "kddcup_data.csv")

# 📌 Create "data" directory if it does not exist
if not os.path.exists(DATA_DIR):
    print("📂 Creating data/ directory")
    os.makedirs(DATA_DIR, exist_ok=True)
else:
    print("✅ data/ directory already exists")

# 🔽 Step 1: Download files
def download_file(url, output_file):
    if os.path.exists(output_file):
        print(f"✅ File already downloaded: {output_file}")
        return
    
    print(f"🔽 Downloading {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print(f"✅ Download complete: {output_file}")
    else:
        print(f"❌ ERROR: Could not download {url}. Status code {response.status_code}")

# 🗜️ Step 2: Decompress .gz file
def decompress_gz(input_file, output_file):
    if os.path.exists(output_file):
        print(f"✅ File already decompressed: {output_file}")
        return
    
    print("🗜️ Decompressing file...")
    if os.path.exists(input_file):
        with gzip.open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"✅ File decompressed: {output_file}")
    else:
        print(f"❌ ERROR: File not found {input_file}")

# 📊 Step 3: Convert to CSV with column names
def convert_to_csv(input_file, output_csv):
    print("📊 Processing data and converting to CSV...")

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
        print(f"✅ Data saved in {output_csv}")
    else:
        print(f"❌ ERROR: File not found {input_file}")

# 🛠️ Step 4: Execute the complete pipeline
if __name__ == "__main__":
    print("🚀 Starting download and conversion process...")

    # 1. Download files
    download_file(URL_DATA, RAW_FILE_GZ)
    download_file(URL_NAMES, os.path.join(DATA_DIR, "kddcup.names"))

    # 2. Decompress the dataset
    decompress_gz(RAW_FILE_GZ, RAW_FILE)

    # 3. Convert to CSV
    convert_to_csv(RAW_FILE, CSV_FILE)

    # 4. Remove temporary files (optional)
    if os.path.exists(RAW_FILE): os.remove(RAW_FILE)
    if os.path.exists(RAW_FILE_GZ): os.remove(RAW_FILE_GZ)
    print("🗑️ Temporary files deleted.")
