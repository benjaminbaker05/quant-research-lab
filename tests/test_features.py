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
    assert "future_return_1d" in features.columns
    assert "volatility_20" in features.columns
    assert len(features) > 0


def test_target_matches_next_day_return(tmp_path):
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

    # Every retained observation must have a known future return.
    assert features["future_return_1d"].notna().all()

    # target_up must exactly represent whether the next-day return is positive.
    expected_target = (features["future_return_1d"] > 0).astype(int)

    pd.testing.assert_series_equal(
        features["target_up"],
        expected_target,
        check_names=False,
    )


def test_final_source_observation_is_not_used_as_target(tmp_path):
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

    # The source dataset's final row has no next-day return,
    # so it must not appear in the feature dataset.
    assert features["date"].max() < df["date"].max()
