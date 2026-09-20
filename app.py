import streamlit as st

from data import load_sales_data

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    df = load_sales_data(DATA_PATH)
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()
