import pandas as pd

from src.features.build_features import build_features


def test_build_features_creates_target(tmp_path):
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=40),
            "open": range(100, 140),
            "high": range(101, 141),
            "low": range(99, 139),
            "close": range(100, 140),
            "volume": range(1000, 1040),
        }
    )

    input_path = tmp_path / "sample.parquet"
    df.to_parquet(input_path, index=False)

    features = build_features(input_path)

    assert "target_up" in features.columns
    assert "return_1d" in features.columns
    assert "volatility_20" in features.columns
    assert len(features) > 0