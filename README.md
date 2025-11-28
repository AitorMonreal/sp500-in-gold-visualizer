# S&P 500 Priced in Gold Visualization

This project visualizes the S&P 500 index priced in Gold (oz) since the 1970s.

## Setup

1.  **Install Miniconda** (if not already installed).
2.  **Create the environment**:
    ```bash
    conda env create -f environment.yml
    ```
3.  **Activate the environment**:
    ```bash
    conda activate finance-sp500-gold
    ```

## Usage

1.  **Download and Process Data**:

    ```bash
    python download_data.py
    ```

    This will generate `data.json`.

2.  **Run Tests**:

    ```bash
    pytest test_data_processing.py
    ```

3.  **View Visualization**:
    Open `index.html` in your web browser.

## Data Sources

- **S&P 500**: `yfinance` (`^GSPC`) - Daily.
- **Gold**:
  - 1950-2000: GitHub (`monthly.csv`) - Monthly.
  - 2000-Present: `yfinance` (`GC=F`) - Daily.
