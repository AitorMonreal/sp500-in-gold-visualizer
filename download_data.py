import yfinance as yf
import pandas as pd
import requests
import io
import json


def download_sp500():
    """Download S&P 500 daily data from yfinance."""
    print("Downloading S&P 500 data...")
    sp500 = yf.Ticker("^GSPC")
    hist = sp500.history(period="max")
    hist = hist[["Close"]]
    hist.index = hist.index.tz_localize(None)
    hist.columns = ["SP500"]
    return hist


def download_gold_monthly():
    """Download historical monthly gold data from GitHub."""
    print("Downloading historical monthly Gold data...")
    url = (
        "https://raw.githubusercontent.com/datasets/gold-prices/master/data/monthly.csv"
    )
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")
        df.columns = ["Gold"]
        return df
    else:
        raise Exception(f"Failed to download monthly gold data: {response.status_code}")


def download_gold_daily():
    """Download recent daily gold data from yfinance."""
    print("Downloading daily Gold data...")
    gold = yf.Ticker("GC=F")
    hist = gold.history(period="max")
    hist = hist[["Close"]]
    hist.index = hist.index.tz_localize(None)
    hist.columns = ["Gold"]
    return hist


def process_data():
    """Download, merge, and process data."""
    # 1. Get Data
    sp500 = download_sp500()
    gold_monthly = download_gold_monthly()
    gold_daily = download_gold_daily()

    # 2. Combine Gold Data
    # Determine the start of daily data
    if not gold_daily.empty:
        cutoff_date = gold_daily.index[0]
        print(f"Daily Gold data starts at: {cutoff_date}")
    else:
        # Fallback if daily data fails (though it shouldn't based on previous checks)
        cutoff_date = pd.Timestamp("2025-01-01")

    # Use monthly data strictly BEFORE the daily data starts
    gold_monthly_pre_daily = gold_monthly[gold_monthly.index < cutoff_date]

    # Resample monthly to daily and interpolate
    # We extend interpolation up to the cutoff date to bridge any gap
    gold_monthly_daily = gold_monthly_pre_daily.resample("D").interpolate(
        method="linear"
    )

    # Handle the gap: The monthly data might end before the daily data starts if we just cut it off.
    # We need to ensure we interpolate UP TO the daily data start.
    # Let's re-index the monthly data to include the cutoff date (if not present) to allow interpolation to reach it.

    # Better approach:
    # 1. Take all monthly data.
    # 2. Resample to daily.
    # 3. Cut off at cutoff_date.

    gold_monthly_daily_full = gold_monthly.resample("D").interpolate(method="linear")
    gold_monthly_part = gold_monthly_daily_full[
        gold_monthly_daily_full.index < cutoff_date
    ]

    # Combine
    gold_combined = pd.concat([gold_monthly_part, gold_daily])
    gold_combined = gold_combined.sort_index()

    # 3. Merge S&P 500 and Gold
    merged = pd.merge(
        sp500, gold_combined, left_index=True, right_index=True, how="inner"
    )

    # 4. Calculate Ratio
    merged["Ratio"] = merged["SP500"] / merged["Gold"]

    # 5. Filter for Modern Floating-Price Era (post-1971 approx, but we have data since 1950s)
    # User asked for "since around the 1970s-1980s". Let's start from 1970.
    start_date = pd.Timestamp("1970-01-01")
    merged = merged[merged.index >= start_date]

    # 6. Format for JSON
    output_data = []
    for date, row in merged.iterrows():
        output_data.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "sp500": round(row["SP500"], 2),
                "gold": round(row["Gold"], 2),
                "ratio": round(row["Ratio"], 4),
            }
        )

    return output_data


if __name__ == "__main__":
    try:
        data = process_data()
        with open("data.json", "w") as f:
            json.dump(data, f)
        print(f"Successfully processed {len(data)} data points. Saved to data.json.")
    except Exception as e:
        print(f"Error processing data: {e}")
