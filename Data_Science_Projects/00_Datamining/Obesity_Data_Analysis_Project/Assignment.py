# importing libraries 
import os
import sys
import json
import random 
import platform 
from pathlib import Path
from itertools import combinations 

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

SEED   = 42
random.seed(SEED)
np.random.seed(SEED)

# Creating Project Structure 

PROJECT_ROOT    = Path.cwd() / "00_Introduction" / "00_Datamining"
DATA_RAW        = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED  = PROJECT_ROOT / "data" / "processed"
DATA_INTERIM    = PROJECT_ROOT / "data" / "interim"
REPORTS         = PROJECT_ROOT / "reports"
CONFIGS         = PROJECT_ROOT / "configs"
MODELS          = PROJECT_ROOT / "models"

def print_environment() -> None:
    print(f"Python:  {sys.version.split()[0]}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"NumPy: {np.__version__}")
    print(f"Pandas: {pd.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"Seaborn: {sns.__version__}")
    print(f"SciPy: {stats.__version__}")

# Creating Project Folders 

for folder in [DATA_RAW, DATA_PROCESSED, DATA_INTERIM, REPORTS, CONFIGS, MODELS]:
   folder.mkdir(parents=True, exist_ok=True)
   print(f" Created : {folder.relative_to(PROJECT_ROOT)}")

print(f"\n  Project root: {PROJECT_ROOT}")
print(f"   Status: {'Ready' if PROJECT_ROOT.exists() else 'Failed'}")   

# Writing README file

def write_readme():
    readme = "# Obesity_Data_Analysis_Project"
    (PROJECT_ROOT / 'README.md').write_text(readme)
    print("Wrote :", PROJECT_ROOT / 'README.md')

# writing requirements file

def write_requirements():
    requirements = [
        f"NumPy=={np.__version__}",
        f"Pandas=={pd.__version__}",
        f"Matplotlib=={matplotlib.__version__}",
        f"Seaborn=={sns.__version__}",
        f"SciPy=={stats.__version__}"
    ]
    (PROJECT_ROOT / "REQUIREMENTS.txt").write_text(
        "\n".join(requirements) + "\n"
    )
    print("Wrote :", PROJECT_ROOT / "REQUIREMENTS.txt")

# writing config file 

def write_config():
    config = {
        "project_name": "Obesity Data Analysis",
        "author": "Your Name",
        "version": "0.1.0",
        "description": "A project to analyze obesity data and identify key factors.",
        "data_sources": {
            "raw_data": str(DATA_RAW),
            "processed_data": str(DATA_PROCESSED),
            "interim_data": str(DATA_INTERIM)
        },
        "reports": str(REPORTS),
        "models": str(MODELS)
    }
    (CONFIGS / "config.json").write_text(json.dumps(config, indent=4))
    print("Wrote :", CONFIGS / "config.json")

# cNot necessaritly but recommended 










        
