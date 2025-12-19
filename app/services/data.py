import pandas as pd
import os
from core.config import settings
import logging

logger = logging.getLogger(__name__)

DATA_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
DATA_FILE = "data/nyc_311.csv"

def load_data(limit: int = 100000):
    """
    Load data from local CSV or download from NYC Open Data if missing.
    Args:
        limit: Number of records to fetch if downloading (default 100k to avoid timeouts).
               In production, we might want to fetch more or use pagination.
    """
    if os.path.exists(DATA_FILE):
        logger.info(f"Loading data from {DATA_FILE}")
        # Low_memory=False to avoid mixed type warnings on large files
        df = pd.read_csv(DATA_FILE, low_memory=False)
        # Ensure created_date is datetime if it exists
        if 'Created Date' in df.columns: # Kaggle dataset usually has 'Created Date'
             df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
        elif 'created_date' in df.columns:
            df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
            
        return df
    
    raise FileNotFoundError(f"Data file not found at {DATA_FILE}. Please download the dataset from Kaggle and place it in 'data/nyc_311.csv'.")
