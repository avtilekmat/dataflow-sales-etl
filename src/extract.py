import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def extract_data():
    csv_path = BASE_DIR / "data" / "sales.csv"

    df= pd.read_csv(csv_path)

    return df


if __name__ == "__main__":
    result = extract_data()
    print(result.head())