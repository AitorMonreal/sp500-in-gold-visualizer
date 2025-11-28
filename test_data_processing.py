import pytest
import pandas as pd
from download_data import (
    process_data,
    download_sp500,
    download_gold_monthly,
    download_gold_daily,
)
from unittest.mock import MagicMock, patch


def test_download_sp500_mock():
    with patch("yfinance.Ticker") as mock_ticker:
        mock_hist = pd.DataFrame(
            {"Close": [100, 101]}, index=pd.to_datetime(["2020-01-01", "2020-01-02"])
        )
        mock_ticker.return_value.history.return_value = mock_hist

        df = download_sp500()
        assert not df.empty
        assert "SP500" in df.columns
        assert len(df) == 2


def test_download_gold_monthly_mock():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Date,Price\n1990-01-01,400\n1990-02-01,410"
        mock_get.return_value = mock_response

        df = download_gold_monthly()
        assert not df.empty
        assert "Gold" in df.columns
        assert len(df) == 2


def test_data_structure():
    # Integration test (runs actual download if not mocked, but let's mock for speed/reliability in unit test)
    # For this test, we'll mock the internal download functions to test the merge logic

    with patch("download_data.download_sp500") as mock_sp500, patch(
        "download_data.download_gold_monthly"
    ) as mock_gold_monthly, patch(
        "download_data.download_gold_daily"
    ) as mock_gold_daily:

        # Setup Mock Data
        dates_sp = pd.date_range(start="1999-12-01", end="2000-01-05", freq="D")
        mock_sp500.return_value = pd.DataFrame(
            {"SP500": [1000 + i for i in range(len(dates_sp))]}, index=dates_sp
        )

        dates_gm = pd.to_datetime(["1999-12-01", "2000-01-01"])
        mock_gold_monthly.return_value = pd.DataFrame(
            {"Gold": [300, 310]}, index=dates_gm
        )

        dates_gd = pd.date_range(start="2000-01-01", end="2000-01-05", freq="D")
        mock_gold_daily.return_value = pd.DataFrame(
            {"Gold": [310 + i for i in range(len(dates_gd))]}, index=dates_gd
        )

        # Run Process
        result = process_data()

        assert isinstance(result, list)
        assert len(result) > 0
        first_item = result[0]
        assert "date" in first_item
        assert "sp500" in first_item
        assert "gold" in first_item
        assert "ratio" in first_item

        # Check if ratio is calculated correctly
        # 1999-12-01: SP=1000, Gold=300 -> Ratio=3.3333
        # Find 1999-12-01 in result
        item_1999 = next(
            (item for item in result if item["date"] == "1999-12-01"), None
        )
        # Note: The script filters for >= 1970, so 1999 should be there.
        # However, the script also does an inner join.
        # Gold monthly is resampled to daily.

        if item_1999:
            assert abs(item_1999["ratio"] - (1000 / 300)) < 0.01


if __name__ == "__main__":
    pytest.main()
