import yfinance as yf
import pandas as pd

def get_stock_data(symbols):
    data = []
    for symbol in symbols:
        try:
            info = yf.Ticker(symbol).info

            current = info.get('currentPrice')
            high = info.get('fiftyTwoWeekHigh')
            low = info.get('fiftyTwoWeekLow')
            pe = info.get('trailingPE')
            cap = info.get('marketCap')
            sector = info.get('sector', 'N/A')

            diff = round(((current - high) / high) * 100, 2) if current and high else None

            data.append({
                "Stock": symbol.replace(".NS", ""),
                "Current Price (₹)": current,
                "52W High (₹)": high,
                "52W Low (₹)": low,
                "From 52W High (%)": diff,
                "PE Ratio": pe,
                "Market Cap": cap,
                "Sector": sector
            })
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    return pd.DataFrame(data)
