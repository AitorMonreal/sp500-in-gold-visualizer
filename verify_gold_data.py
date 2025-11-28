import pandas as pd
import requests
import io


def get_csv(url, name):
    try:
        print(f"Downloading {name} from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_csv(io.StringIO(response.text))
        else:
            print(f"Failed to download {name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {name}: {e}")
        return None


github_url = (
    "https://raw.githubusercontent.com/datasets/gold-prices/master/data/monthly.csv"
)
datahub_url = "https://datahub.io/core/gold-prices/_r/-/data/monthly.csv"

df_github = get_csv(github_url, "GitHub")
df_datahub = get_csv(datahub_url, "DataHub")

if df_github is not None and df_datahub is not None:
    # Normalize dates
    df_github["Date"] = pd.to_datetime(df_github["Date"])
    df_datahub["Date"] = pd.to_datetime(df_datahub["Date"])

    # Rename columns for merge
    df_github = df_github.rename(columns={"Price": "Price_GitHub"})
    df_datahub = df_datahub.rename(columns={"Price": "Price_DataHub"})

    # Merge
    merged = pd.merge(df_github, df_datahub, on="Date", how="inner")

    print(f"\nMerged Data Points: {len(merged)}")

    # Calculate difference
    merged["Diff"] = merged["Price_GitHub"] - merged["Price_DataHub"]
    merged["AbsDiff"] = merged["Diff"].abs()

    print(f"Mean Absolute Difference: {merged['AbsDiff'].mean():.4f}")
    print(f"Max Absolute Difference: {merged['AbsDiff'].max():.4f}")

    # Check specific dates
    print("\nSample Comparisons:")
    print(merged.sample(5))

    if merged["AbsDiff"].mean() < 1.0:
        print("\nVERIFICATION SUCCESSFUL: Data sources are consistent.")
    else:
        print("\nVERIFICATION WARNING: Significant differences found.")
else:
    print("\nVERIFICATION FAILED: Could not download one or both datasets.")
