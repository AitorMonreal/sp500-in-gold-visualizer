# Project Context: S&P 500 Priced in Gold Visualizer

## 1. Project Objective

To visualize the historical performance of the S&P 500 index priced in ounces of Gold, specifically focusing on the "Modern Floating-Price Era" (post-1971) to the present day. The goal is to provide a professional, interactive web-based chart that updates daily.

## 2. Architecture & Tech Stack

- **Backend / ETL**: Python (pandas, yfinance).
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+).
- **Visualization**: Chart.js with `chartjs-adapter-date-fns` and `chartjs-plugin-zoom`.
- **Infrastructure**: GitHub Pages (Hosting) + GitHub Actions (Automation).
- **Package Management**: pip (`requirements.txt`) and Conda (`environment.yml`).

## 3. Data Pipeline (`download_data.py`)

The core logic resides in a Python script that aggregates and processes data from two disparate sources to create a continuous daily time series.

### Data Sources

1.  **S&P 500 (`^GSPC`)**:
    - Source: Yahoo Finance (`yfinance`).
    - Frequency: Daily.
    - Range: 1927 - Present.
2.  **Gold Price**:
    - **Historical (1950 - ~2000)**: Monthly data from GitHub Datasets (`gold-prices/monthly.csv`). Verified for accuracy against DataHub.
    - **Modern (2000 - Present)**: Daily data from Yahoo Finance (`GC=F`).

### Processing Logic

1.  **Ingestion**: Fetches S&P 500 daily data and both Gold datasets.
2.  **Harmonization**:
    - Identifies the start date of the Daily Gold data (approx. Aug 30, 2000).
    - Slices the Monthly Gold data to end strictly _before_ the Daily data starts.
    - **Interpolation**: Resamples the Monthly Gold data to Daily frequency using linear interpolation to match the S&P 500's granularity.
    - Concatenates the interpolated historical data with the modern daily data to form a single `Gold` series.
3.  **Calculation**: Merges S&P 500 and Gold series on their Date index and calculates the ratio: `Ratio = SP500_Close / Gold_Close`.
4.  **Cleaning**: Filters for data starting from Jan 1, 1970.
5.  **Output**: Exports the processed time series to a lightweight JSON file (`data.json`) optimized for the frontend.

### Automation

- **GitHub Actions**: A workflow (`.github/workflows/daily_update.yml`) runs daily at 00:00 UTC.
- It executes `download_data.py`, commits any changes to `data.json`, and pushes to the repository, triggering a GitHub Pages rebuild.

## 4. Frontend Application

- **`index.html`**: Semantic structure with a chart container and control overlay.
- **`script.js`**:
  - Asynchronously fetches `data.json`.
  - Renders a responsive Chart.js line graph.
  - Implements a custom "Golden Gradient" fill for visual aesthetics.
  - Configures interaction: Zooming (wheel/pinch), Panning, and sophisticated Tooltips showing refined Date/Value pairs.
- **`style.css`**: Professional "Dark Mode" aesthetic using specific gold hex codes (`#FFD700`, `#DAA520`) against dark backgrounds (`#121212`, `#1E1E1E`). Responsive layout for mobile/desktop.

## 5. Verification & Testing

- **Unit Tests**: `test_data_processing.py` (pytest) verifies download functions (mocked) and data merging logic.
- **Gap Analysis**: `verify_gap.py` was built to detect and verify the resolution of data gaps, specifically a previously identified gap between the monthly/daily transition in 1999-2000. Confirmed < 7 day gaps (standard market holidays/9-11 closure).

## 6. Access

- **Local**: `python -m http.server 8000`
- **Production**: Hosted via GitHub Pages on the `main` branch.
