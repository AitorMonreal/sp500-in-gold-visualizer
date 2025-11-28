import yfinance as yf
import pandas as pd
import io
import requests


def check_yfinance(ticker, name):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="max")
        if not hist.empty:
            print(f"{name} ({ticker}) Start Date: {hist.index[0]}")
            print(f"{name} ({ticker}) End Date: {hist.index[-1]}")
            print(f"{name} ({ticker}) Rows: {len(hist)}")
        else:
            print(f"{name} ({ticker}) No data found.")
    except Exception as e:
        print(f"Error checking {name} ({ticker}): {e}")


def check_url_csv(url, name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            print(f"{name} (CSV) Columns: {df.columns.tolist()}")
            print(f"{name} (CSV) Rows: {len(df)}")
            if "Date" in df.columns:
                print(f"{name} (CSV) Start Date: {df['Date'].min()}")
                print(f"{name} (CSV) End Date: {df['Date'].max()}")
            elif "date" in df.columns:
                print(f"{name} (CSV) Start Date: {df['date'].min()}")
                print(f"{name} (CSV) End Date: {df['date'].max()}")
        else:
            print(f"{name} (CSV) Failed to download: {response.status_code}")
    except Exception as e:
        print(f"Error checking {name} (CSV): {e}")


print("--- Checking YFinance ---")
check_yfinance("^GSPC", "S&P 500")
check_yfinance("GC=F", "Gold Futures")
check_yfinance("XAUUSD=X", "Gold Spot (USD)")

print("\n--- Checking DataHub ---")
check_url_csv(
    "https://pkgstore.datahub.io/core/gold-prices/monthly_csv/data/9d6774a9af353220f6e43f96d29d602f/monthly_csv.csv",
    "Gold Monthly (DataHub)",
)
