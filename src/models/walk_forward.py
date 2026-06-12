from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "return_1d",
    "log_return_1d",
    "volatility_5",
    "volatility_20",
    "volume_change_1d",
    "close_to_ma_5",
    "close_to_ma_20",
]


@dataclass
class WalkForwardResult:
    model_name: str
    predictions: pd.DataFrame
    metrics: dict[str, float]


def get_model_candidates(random_state: int = 42) -> dict[str, object]:
    """
    Return simple model candidates for time-series classification.

    These are deliberately modest models. The goal is to compare against
    simple baselines before trying anything more complex.
    """
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000)),
            ]
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=5,
            min_samples_leaf=20,
            random_state=random_state,
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=100,
            learning_rate=0.05,
            max_leaf_nodes=15,
            random_state=random_state,
        ),
    }


def validate_ml_dataframe(
    df: pd.DataFrame,
    feature_columns: list[str],
    target_column: str,
) -> None:
    """
    Validate that the dataframe contains the required ML columns.
    """
    required_columns = ["date", *feature_columns, target_column]

    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("Input dataframe is empty")


def calculate_prediction_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    y_prob: pd.Series,
) -> dict[str, float]:
    """
    Calculate classification metrics for out-of-sample predictions.
    """
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }

    # ROC AUC is undefined if the test labels contain only one class.
    if len(set(y_true)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
    else:
        metrics["roc_auc"] = 0.0

    return metrics


def walk_forward_predict(
    df: pd.DataFrame,
    model: object,
    model_name: str,
    feature_columns: list[str] | None = None,
    target_column: str = "target_up",
    min_train_size: int = 500,
    test_size: int = 63,
    step_size: int = 63,
) -> WalkForwardResult:
    """
    Train and evaluate a model using walk-forward validation.

    At each fold:
    - train on all data up to time t
    - predict on the next test window
    - move forward in time

    This avoids random train/test splitting, which would leak future information
    in a time-series setting.
    """
    if feature_columns is None:
        feature_columns = FEATURE_COLUMNS

    validate_ml_dataframe(
        df=df,
        feature_columns=feature_columns,
        target_column=target_column,
    )

    if min_train_size <= 0:
        raise ValueError("min_train_size must be positive")

    if test_size <= 0:
        raise ValueError("test_size must be positive")

    if step_size <= 0:
        raise ValueError("step_size must be positive")

    df = df.sort_values("date").reset_index(drop=True).copy()

    if len(df) <= min_train_size:
        raise ValueError(
            "Not enough rows for walk-forward validation. "
            f"Rows: {len(df)}, min_train_size: {min_train_size}"
        )

    prediction_frames = []
    fold = 0
    start = min_train_size

    while start < len(df):
        end = min(start + test_size, len(df))

        train = df.iloc[:start].copy()
        test = df.iloc[start:end].copy()

        X_train = train[feature_columns]
        y_train = train[target_column]

        X_test = test[feature_columns]
        y_test = test[target_column]

        fitted_model = clone(model)
        fitted_model.fit(X_train, y_train)

        if hasattr(fitted_model, "predict_proba"):
            y_prob = fitted_model.predict_proba(X_test)[:, 1]
        else:
            y_prob = fitted_model.predict(X_test)

        y_pred = (y_prob >= 0.5).astype(int)

        predictions = pd.DataFrame(
            {
                "date": test["date"].values,
                "fold": fold,
                "model_name": model_name,
                "y_true": y_test.values,
                "y_prob": y_prob,
                "y_pred": y_pred,
            }
        )

        prediction_frames.append(predictions)

        fold += 1
        start += step_size

    all_predictions = pd.concat(prediction_frames, ignore_index=True)

    metrics = calculate_prediction_metrics(
        y_true=all_predictions["y_true"],
        y_pred=all_predictions["y_pred"],
        y_prob=all_predictions["y_prob"],
    )

    return WalkForwardResult(
        model_name=model_name,
        predictions=all_predictions,
        metrics=metrics,
    )


def probability_to_signal(
    probabilities: pd.Series,
    long_threshold: float = 0.53,
    short_threshold: float = 0.47,
) -> pd.Series:
    """
    Convert predicted probabilities into trading signals.

    - probability > long_threshold: long
    - probability < short_threshold: short
    - otherwise: flat

    The neutral zone avoids trading on weak model confidence.
    """
    if not 0 <= short_threshold <= 1:
        raise ValueError("short_threshold must be between 0 and 1")

    if not 0 <= long_threshold <= 1:
        raise ValueError("long_threshold must be between 0 and 1")

    if short_threshold >= long_threshold:
        raise ValueError("short_threshold must be below long_threshold")

    return pd.Series(
        np.where(
            probabilities > long_threshold,
            1,
            np.where(probabilities < short_threshold, -1, 0),
        ),
        index=probabilities.index,
    )