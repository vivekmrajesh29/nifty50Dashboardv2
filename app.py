from pathlib import Path
import appdirs as ad

# 🔧 Redirect yfinance cache to a writable local folder
CACHE_DIR = ".cache"
ad.user_cache_dir = lambda *args: CACHE_DIR
Path(CACHE_DIR).mkdir(exist_ok=True)

import yfinance as yf
import streamlit as st
import plotly.express as px
from utils.fetch_data import get_stock_data

st.set_page_config(page_title="Nifty 50 Tracker", layout="wide")
st.title("📈 Nifty 50 Stock Fundamentals Dashboard")

# Load stock symbols from file
# try:
#     with open("data/stock_list.txt", "r") as f:
#         stock_list = [line.strip().upper() for line in f if line.strip()]
# except FileNotFoundError:
#     stock_list = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

stock_list = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

symbols_input = st.text_area("Edit symbols (comma-separated):", ", ".join(stock_list))
symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

df = get_stock_data(symbols)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="Stock", y=["Current Price (₹)", "52W High (₹)"],
                 barmode="group", title="Current Price vs 52-Week High")
    st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Show PE Ratio Bubble Chart"):
        pe_df = df.dropna(subset=["PE Ratio"])
        fig2 = px.scatter(pe_df, x="Stock", y="PE Ratio", size="Market Cap",
                          color="Sector", title="PE Ratio & Market Cap by Sector")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data to display. Check your symbols and try again.")
