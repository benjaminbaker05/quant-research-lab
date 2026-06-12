from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def clean_ohlcv(input_path: str | Path) -> Path:
    """
    Clean raw OHLCV CSV data and save it as Parquet.
    """
    input_path = Path(input_path)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    # Handle possible yfinance multi-index export issues.
    df = df.rename(columns={df.columns[0]: "date"})

    required_cols = ["date", "Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[required_cols].copy()
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric_cols = ["open", "high", "low", "close", "volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    df = df.sort_values("date")
    df = df.drop_duplicates(subset=["date"])

    output_path = PROCESSED_DATA_DIR / input_path.with_suffix(".parquet").name
    df.to_parquet(output_path, index=False)

    return output_path


if __name__ == "__main__":
    raw_files = list(RAW_DATA_DIR.glob("*.csv"))

    if not raw_files:
        raise FileNotFoundError("No raw CSV files found in data/raw")

    for raw_file in raw_files:
        output = clean_ohlcv(raw_file)
        print(f"Saved cleaned data to {output}")