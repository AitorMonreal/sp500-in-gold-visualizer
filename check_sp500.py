import yfinance as yf

try:
    sp500 = yf.Ticker("^GSPC")
    hist = sp500.history(period="max")
    print(f"S&P 500 Start Date: {hist.index[0]}")
    print(f"S&P 500 End Date: {hist.index[-1]}")
    print(hist.head())
except Exception as e:
    print(f"Error getting S&P 500 data: {e}")
