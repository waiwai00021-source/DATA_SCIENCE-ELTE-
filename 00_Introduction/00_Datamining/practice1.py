import os 
import sys
import platform 
import json
import random 

from pathlib import Path 

import numpy as np
import pandas as pd

def main() -> None:
    print("Python :", sys.version.split()[0])
    print("Platform :", platform.platform())
    print("NumPy :", np.__version__)
    print("Pandas :", pd.__version__)

if __name__ == "__main__":
    main()

# Creating Project Structure 

PROJECT_ROOT      = Path.cwd() / "00_Introduction" / "00_Datamining"
DATA_RAW          = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED    = PROJECT_ROOT / "data" / "processed"
DATA_INTERIM      = PROJECT_ROOT / "data" / "interim"
REPORTS           = PROJECT_ROOT / "reports"
CONFIGS           = PROJECT_ROOT / "configs"
MODELS            = PROJECT_ROOT / "models"

for p in [DATA_RAW, DATA_PROCESSED, DATA_INTERIM, REPORTS, CONFIGS, MODELS]:
    p.mkdir(parents=True, exist_ok=True)
    print(f" Created {p.relative_to(PROJECT_ROOT)}")

print(f" Created :", (PROJECT_ROOT))
print(f" Status:", "'Ready" if PROJECT_ROOT.exists() else "Failed")

# writing readme file 
readme = """ # Data Mining Homework 1

"""
(PROJECT_ROOT / "READEME.md").write_text(readme)
print("Wrote :", PROJECT_ROOT / "READEME.md")

PROJECT_ROOT 

# writing requriements file 

requirements   = [
    (f"NumPy =={np.__version__}"),
    (f"Pandas =={pd.__version__}"),
    "openpxyl"
]
(PROJECT_ROOT / "REQUIREMENTS.txt").write_text("\n".join(requirements)+"\n")
print("Wrote :", PROJECT_ROOT / "REQUIREMENTS.txt")

# Random Control 
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
    "models": str(MODELS)               
}
(PROJECT_ROOT / "CONFIGS.json").write_text(json.dumps(configs, indent=4))
print("Wrote :", PROJECT_ROOT / "CONFIGS.json") 

# Saving cs