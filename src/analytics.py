import pandas as pd


def analyze_sales(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "orders": 0,
            "revenue": 0.0,
            "average_order": 0.0,
            "products_sold": 0
        }

    return {
        "orders": len(df),
        "revenue": float(df["total_price"].sum()),
        "average_order": float(df["total_price"].mean()),
        "products_sold": int(df["quantity"].sum())
    }
