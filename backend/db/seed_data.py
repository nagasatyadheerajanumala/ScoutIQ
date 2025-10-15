import zipfile, os, pandas as pd

import sqlalchemy
from click import clear
from sqlalchemy import create_engine
from sqlalchemy.types import Float, String, Date, Boolean

DATABASE_URL = "postgresql://dheeraj@localhost/scoutiq"
engine = create_engine(DATABASE_URL)

DATA_PATH = "/Users/dheeraj/Desktop/ScoutIQ/data"   # folder containing your ZIP files

def extract_zip_files():
    for file in os.listdir(DATA_PATH):
        if file.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(DATA_PATH, file), 'r') as z:
                z.extractall(DATA_PATH)
            print(f"✅ Extracted: {file}")


def load_csv_to_db(csv_path, table_name, chunksize=5000):
    print(f"📦 Streaming {table_name} to database in chunks...")

    print("🔍 Scanning CSV headers to unify schema...")
    all_cols = pd.read_csv(csv_path, nrows=0, low_memory=False).columns.tolist()
    print(f"✅ Detected {len(all_cols)} columns.")

    i = 0
    for chunk in pd.read_csv(
            csv_path,
            chunksize=chunksize,
            low_memory=False,
            dtype=str,  # all strings
            na_values=["", " ", "NULL", "NaN", "N/A", "#N/A"],
            keep_default_na=True,
            encoding_errors="ignore",  # 👈 ignore bad characters
            encoding="utf-8",  # try UTF-8 first
    ):
        # 🔄 Normalize schema
        for col in all_cols:
            if col not in chunk.columns:
                chunk[col] = None
        chunk = chunk[all_cols]

        # 🧹 Clean whitespace
        chunk = chunk.map(lambda x: x.strip() if isinstance(x, str) else x, na_action='ignore')

        # 🔒 Cast everything to string before loading
        chunk = chunk.astype(str)

        try:
            chunk.to_sql(
                table_name,
                engine,
                if_exists="append" if i > 0 else "replace",
                index=False,
                dtype={col: sqlalchemy.types.Text() for col in all_cols},  # 👈 KEY FIX
            )
            i += 1
            print(f"  ✅ Loaded {i * chunksize:,} rows so far...")
        except Exception as e:
            print(f"⚠️ Skipped chunk due to error: {e}")
            continue

    print(f"✅ Finished loading {table_name}")

def run_loader():
    extract_zip_files()
    for file in os.listdir(DATA_PATH):
        if file.endswith(".csv"):
            name = os.path.basename(file).split(".")[0].lower()
            load_csv_to_db(os.path.join(DATA_PATH, file), name)
clear()
if __name__ == "__main__":
    run_loader()