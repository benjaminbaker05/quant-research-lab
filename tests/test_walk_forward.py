import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models.walk_forward import (
    calculate_prediction_metrics,
    probability_to_signal,
    walk_forward_predict,
)


def make_sample_ml_dataframe(n_rows: int = 120) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=n_rows),
            "return_1d": [0.01, -0.01] * (n_rows // 2),
            "log_return_1d": [0.01, -0.01] * (n_rows // 2),
            "volatility_5": [0.02] * n_rows,
            "volatility_20": [0.03] * n_rows,
            "volume_change_1d": [0.01, 0.02] * (n_rows // 2),
            "close_to_ma_5": [0.01, -0.01] * (n_rows // 2),
            "close_to_ma_20": [0.02, -0.02] * (n_rows // 2),
            "target_up": [1, 0] * (n_rows // 2),
        }
    )


def test_probability_to_signal_creates_long_short_flat():
    probabilities = pd.Series([0.6, 0.5, 0.4])

    signals = probability_to_signal(
        probabilities,
        long_threshold=0.55,
        short_threshold=0.45,
    )

    assert list(signals) == [1, 0, -1]


def test_probability_to_signal_rejects_bad_thresholds():
    probabilities = pd.Series([0.5, 0.6])

    with pytest.raises(ValueError):
        probability_to_signal(
            probabilities,
            long_threshold=0.4,
            short_threshold=0.6,
        )


def test_calculate_prediction_metrics_outputs_expected_keys():
    y_true = pd.Series([1, 0, 1, 0])
    y_pred = pd.Series([1, 0, 0, 0])
    y_prob = pd.Series([0.8, 0.2, 0.4, 0.3])

    metrics = calculate_prediction_metrics(
        y_true=y_true,
        y_pred=y_pred,
        y_prob=y_prob,
    )

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert "roc_auc" in metrics


def test_walk_forward_predict_outputs_predictions():
    df = make_sample_ml_dataframe(n_rows=120)

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000)),
        ]
    )

    result = walk_forward_predict(
        df=df,
        model=model,
        model_name="test_model",
        min_train_size=60,
        test_size=20,
        step_size=20,
    )

    assert result.model_name == "test_model"
    assert not result.predictions.empty
    assert "y_prob" in result.predictions.columns
    assert "y_pred" in result.predictions.columns
    assert "accuracy" in result.metrics