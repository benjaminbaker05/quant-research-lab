import pandas as pd

from src.data.clean import clean_ohlcv


def test_clean_ohlcv_outputs_expected_columns(tmp_path):
    raw = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=5),
            "Open": [1, 2, 3, 4, 5],
            "High": [2, 3, 4, 5, 6],
            "Low": [0, 1, 2, 3, 4],
            "Close": [1.5, 2.5, 3.5, 4.5, 5.5],
            "Volume": [100, 200, 300, 400, 500],
        }
    )

    input_path = tmp_path / "raw.csv"
    raw.to_csv(input_path, index=False)

    output_path = clean_ohlcv(input_path)
    cleaned = pd.read_parquet(output_path)

    assert list(cleaned.columns) == [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    assert len(cleaned) == 5