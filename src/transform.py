import pandas as pd
from src.extract import extract_data


def transform_data(df):
    df = df.drop_duplicates(subset=["order_id"])

    df = df.dropna(subset=["order_id", "price", "quantity"])

    df = df[(df["price"] > 0) & (df["quantity"] > 0)]

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    df["total_price"] = df["price"] * df["quantity"]

    return df

if __name__ == "__main__":
    df = extract_data()
    result = transform_data(df)
    print(result.head())