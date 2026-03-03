import sys
import random
import platform
from pathlib import Path

import numpy as np
import pandas as pd

def main() -> None:
    print("Python:", sys.version.split()[0])
    print("Platform:", platform.platform())
    print("NumPy:", np.__version__)
    print("Pandas:", pd.__version__)

if __name__ == "__main__":
    main()

# Creating Project Structure 

PROJECT_ROOT   = Path.cwd() / "00_Introduction" / "00_Datamining"
DATA_RAW       = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_INTERIM   = PROJECT_ROOT / "data" / "interim"
REPORTS        = PROJECT_ROOT / "reports"
CONFIGS        = PROJECT_ROOT / "configs"
MODELS         = PROJECT_ROOT / "models"

for p in [ DATA_RAW, DATA_PROCESSED, DATA_INTERIM, REPORTS, CONFIGS, MODELS]:
    p.mkdir(parents=True, exist_ok=True)
    print(f" Created: {p.relative_to(PROJECT_ROOT)}")

print(f"\n  Project root: {PROJECT_ROOT}")
print(f"   Status: {'Ready' if PROJECT_ROOT.exists() else 'Failed'}")

# writing readme file 
readme     = """ # Data Mining Homework 1

"""
(PROJECT_ROOT / 'README.md').write_text(readme)
print("Wrote :", PROJECT_ROOT / 'README.md')

# NOTE: previously had a bare PROJECT_ROOT expression, removed

# writing requirements file 

requirements = [
    f"NumPy=={np.__version__}",
    f"Pandas=={pd.__version__}",
    "openpyxl",    # spelling correction if needed
    "xlrd"          # needed for reading .xls files with pandas
]
(PROJECT_ROOT / "REQUIREMENTS.txt").write_text("\n".join(requirements)+"\n")
print("Wrote :" , PROJECT_ROOT / "REQUIREMENTS.txt")

# random control
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
np.random.random(6)

# writing configs file 

configs = { 
    "seed": SEED,
    "data": {
        "raw": str(DATA_RAW),
        "processed": str(DATA_PROCESSED),
        "interim": str(DATA_INTERIM)
    },
    "reports": str(REPORTS),
    "configs": str(CONFIGS),
    "models": str(MODELS)       
}

# importing json 
import json
(CONFIGS / "config.json").write_text(json.dumps(configs, indent=4))
print(f"✅ Config written: {CONFIGS / 'config.json'}")

# Reading the dataset file 
xls_path = DATA_RAW / "default of credit card clients (2).xls"
if not xls_path.exists():
    print(f"Dataset not found at {xls_path}")
    sys.exit(1)

try:
    # specify engine explicitly to avoid pandas auto-detection issues
    df = pd.read_excel(xls_path, engine="xlrd")
except ImportError:
    print("ERROR: pandas requires the 'xlrd' package to read .xls files.")
    print("Install it with `pip install xlrd` or add it to your requirements.")
    sys.exit(1)

print(df.shape)
print(df.head())
