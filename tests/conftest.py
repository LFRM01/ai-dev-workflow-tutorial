import pandas as pd
import pytest


@pytest.fixture
def sample_sales_df():
    return pd.DataFrame({
        "date": pd.to_datetime([
            "2024-01-05", "2024-01-20", "2024-02-10", "2024-02-15", "2024-03-01",
        ]),
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005"],
        "product": [
            "Wireless Earbuds", "Phone Case", "Smart Watch",
            "USB-C Cable", "Bluetooth Speaker",
        ],
        "category": ["Audio", "Accessories", "Wearables", "Accessories", "Audio"],
        "region": ["North", "South", "East", "West", "North"],
        "quantity": [2, 3, 1, 5, 1],
        "unit_price": [79.99, 24.99, 299.99, 12.99, 149.99],
        "total_amount": [159.98, 74.97, 299.99, 64.95, 149.99],
    })
