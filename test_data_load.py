import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from services.data import load_data

if __name__ == "__main__":
    print("Testing data loading...")
    try:
        df = load_data(limit=1000)
        print(f"Successfully loaded data. Shape: {df.shape}")
        print("Columns:", df.columns.tolist())
        print("Sample data:")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
