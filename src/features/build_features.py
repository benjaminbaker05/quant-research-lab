from pathlib import Path
import numpy as np
import pandas as pd


PROCESSED_DATA_DIR = Path("data/processed")


def build_features(input_path: str | Path) -> pd.DataFrame:
    """
    Build basic time-series features from cleaned OHLCV data.
    """
    input_path = Path(input_path)
    df = pd.read_parquet(input_path)

    df = df.sort_values("date").copy()

    df["return_1d"] = df["close"].pct_change()
    df["log_return_1d"] = np.log(df["close"] / df["close"].shift(1))

    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_20"] = df["close"].rolling(20).mean()

    df["volatility_5"] = df["log_return_1d"].rolling(5).std()
    df["volatility_20"] = df["log_return_1d"].rolling(20).std()

    df["volume_change_1d"] = df["volume"].pct_change()

    df["close_to_ma_5"] = df["close"] / df["ma_5"] - 1
    df["close_to_ma_20"] = df["close"] / df["ma_20"] - 1

    # Prediction target: will tomorrow's return be positive?
    df["future_return_1d"] = df["return_1d"].shift(-1)
    df["target_up"] = (df["future_return_1d"] > 0).astype(int)

    df = df.dropna().reset_index(drop=True)

    return df


if __name__ == "__main__":
    files = list(PROCESSED_DATA_DIR.glob("*.parquet"))

    if not files:
        raise FileNotFoundError("No processed Parquet files found")

    for file in files:
        features = build_features(file)
        output_path = PROCESSED_DATA_DIR / f"features_{file.name}"
        features.to_parquet(output_path, index=False)
        print(f"Saved features to {output_path}")