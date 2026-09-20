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


def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return len(df)


def monthly_sales_trend(df):
    monthly = df.groupby(df["date"].dt.to_period("M"))["total_amount"].sum()
    monthly.index = monthly.index.to_timestamp()
    return monthly.sort_index()
