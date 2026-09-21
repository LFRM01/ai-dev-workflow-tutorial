import pandas as pd
import pytest

from data import (
    load_sales_data,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
    total_orders,
    total_sales,
)


def test_load_sales_data_returns_dataframe_with_parsed_dates(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-05,ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98\n"
    )

    df = load_sales_data(str(csv_path))

    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df.loc[0, "total_amount"] == 159.98


def test_load_sales_data_raises_for_missing_file(tmp_path):
    missing_path = tmp_path / "does-not-exist.csv"

    with pytest.raises(FileNotFoundError):
        load_sales_data(str(missing_path))


def test_load_sales_data_raises_for_missing_required_column(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price\n"
        "2024-01-05,ORD-001,Wireless Earbuds,Audio,North,2,79.99\n"
    )

    with pytest.raises(ValueError):
        load_sales_data(str(csv_path))


def test_total_sales(sample_sales_df):
    assert total_sales(sample_sales_df) == pytest.approx(749.88)


def test_total_orders(sample_sales_df):
    assert total_orders(sample_sales_df) == 5


def test_monthly_sales_trend(sample_sales_df):
    trend = monthly_sales_trend(sample_sales_df)

    assert list(trend.index.strftime("%Y-%m")) == ["2024-01", "2024-02", "2024-03"]
    assert trend.iloc[0] == pytest.approx(234.95)
    assert trend.iloc[1] == pytest.approx(364.94)
    assert trend.iloc[2] == pytest.approx(149.99)


def test_sales_by_category_sorted_descending(sample_sales_df):
    result = sales_by_category(sample_sales_df)

    assert list(result.index) == ["Audio", "Wearables", "Accessories"]
    assert result.iloc[0] == pytest.approx(309.97)


def test_sales_by_region_sorted_descending(sample_sales_df):
    result = sales_by_region(sample_sales_df)

    assert list(result.index) == ["North", "East", "South", "West"]
    assert result.iloc[0] == pytest.approx(309.97)
