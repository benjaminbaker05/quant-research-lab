from pathlib import Path
import yfinance as yf


RAW_DATA_DIR = Path("data/raw")


def download_ohlcv(
    ticker: str,
    start: str,
    end: str,
    interval: str = "1d",
) -> Path:
    """
    Download OHLCV data for a ticker and save it as CSV.

    Parameters
    ----------
    ticker:
        Market ticker, e.g. 'SPY', 'QQQ', 'AAPL'.
    start:
        Start date in YYYY-MM-DD format.
    end:
        End date in YYYY-MM-DD format.
    interval:
        Data interval, e.g. '1d', '1h'.

    Returns
    -------
    Path to saved CSV file.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No data downloaded for {ticker}")

    output_path = RAW_DATA_DIR / f"{ticker}_{interval}_{start}_{end}.csv"
    data.to_csv(output_path)

    return output_path


if __name__ == "__main__":
    path = download_ohlcv(
        ticker="SPY",
        start="2020-01-01",
        end="2025-01-01",
        interval="1d",
    )
    print(f"Saved data to {path}")