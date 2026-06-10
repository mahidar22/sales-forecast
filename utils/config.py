import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
DATA_REPORTS = os.path.join(BASE_DIR, 'data', 'reports')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(DATA_RAW, exist_ok=True)
os.makedirs(DATA_PROCESSED, exist_ok=True)
os.makedirs(DATA_REPORTS, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)