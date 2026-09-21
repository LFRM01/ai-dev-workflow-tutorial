import streamlit as st

from data import (
    load_sales_data,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
    total_orders,
    total_sales,
)
from charts import category_bar_chart, region_bar_chart, trend_line_chart

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    df = load_sales_data(DATA_PATH)
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

if not df.empty:
    st.caption(f"Data from {df['date'].min():%B %Y} to {df['date'].max():%B %Y}")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

st.plotly_chart(trend_line_chart(monthly_sales_trend(df)), use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(category_bar_chart(sales_by_category(df)), use_container_width=True)
col4.plotly_chart(region_bar_chart(sales_by_region(df)), use_container_width=True)
