import os

import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category", "region",
    "quantity", "unit_price", "total_amount",
]


def load_sales_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sales data file not found: {path}")

    df = pd.read_csv(path)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Sales data is missing required columns: {missing_columns}")

    df["date"] = pd.to_datetime(df["date"])
    return df
