from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.backtest.vectorized import run_vectorized_backtest
from src.models.walk_forward import (
    FEATURE_COLUMNS,
    get_model_candidates,
    probability_to_signal,
    walk_forward_predict,
)


PROCESSED_DATA_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame to a markdown table without requiring tabulate.
    """
    columns = list(df.columns)

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []

    for _, row in df.iterrows():
        row_values = [str(row[column]) for column in columns]
        rows.append("| " + " | ".join(row_values) + " |")

    return "\n".join([header, separator, *rows])


def find_feature_file() -> Path:
    feature_files = sorted(PROCESSED_DATA_DIR.glob("features_*.parquet"))

    if not feature_files:
        raise FileNotFoundError(
            "No feature files found. Run python -m src.features.build_features first."
        )

    return feature_files[0]


def run_model_comparison(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run walk-forward validation for each model candidate.
    """
    models = get_model_candidates()

    metric_rows = []
    prediction_frames = []

    for model_name, model in models.items():
        result = walk_forward_predict(
            df=df,
            model=model,
            model_name=model_name,
            feature_columns=FEATURE_COLUMNS,
            target_column="target_up",
            min_train_size=500,
            test_size=63,
            step_size=63,
        )

        row = {
            "model": model_name,
            "accuracy": round(result.metrics["accuracy"], 4),
            "precision": round(result.metrics["precision"], 4),
            "recall": round(result.metrics["recall"], 4),
            "f1": round(result.metrics["f1"], 4),
            "roc_auc": round(result.metrics["roc_auc"], 4),
            "n_predictions": len(result.predictions),
        }

        metric_rows.append(row)
        prediction_frames.append(result.predictions)

    metrics = pd.DataFrame(metric_rows)
    predictions = pd.concat(prediction_frames, ignore_index=True)

    return metrics, predictions


def run_ml_signal_backtests(
    df: pd.DataFrame,
    predictions: pd.DataFrame,
    cost_bps_values: list[float],
) -> pd.DataFrame:
    """
    Convert ML probabilities into trading signals and backtest them.
    """
    backtest_rows = []

    base = df[["date", "future_return_1d"]].copy()
    base["date"] = pd.to_datetime(base["date"])

    predictions = predictions.copy()
    predictions["date"] = pd.to_datetime(predictions["date"])

    for model_name in sorted(predictions["model_name"].unique()):
        model_predictions = predictions[
            predictions["model_name"] == model_name
        ].copy()

        model_predictions["ml_signal"] = probability_to_signal(
            model_predictions["y_prob"],
            long_threshold=0.53,
            short_threshold=0.47,
        )

        backtest_df = model_predictions.merge(
            base,
            on="date",
            how="left",
        )

        for cost_bps in cost_bps_values:
            result = run_vectorized_backtest(
                df=backtest_df,
                signal_column="ml_signal",
                return_column="future_return_1d",
                cost_bps=cost_bps,
            )

            row = {
                "model": model_name,
                "cost_bps": cost_bps,
                "cumulative_return": round(
                    result.metrics["cumulative_return"],
                    4,
                ),
                "annualised_return": round(
                    result.metrics["annualised_return"],
                    4,
                ),
                "annualised_volatility": round(
                    result.metrics["annualised_volatility"],
                    4,
                ),
                "sharpe_ratio": round(
                    result.metrics["sharpe_ratio"],
                    4,
                ),
                "max_drawdown": round(
                    result.metrics["max_drawdown"],
                    4,
                ),
                "hit_rate": round(
                    result.metrics["hit_rate"],
                    4,
                ),
                "average_turnover": round(
                    result.metrics["average_turnover"],
                    4,
                ),
            }

            backtest_rows.append(row)

    return pd.DataFrame(backtest_rows)


def save_probability_plot(
    predictions: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Save a plot of model probabilities through time.
    """
    predictions = predictions.copy()
    predictions["date"] = pd.to_datetime(predictions["date"])

    plt.figure(figsize=(10, 6))

    for model_name in sorted(predictions["model_name"].unique()):
        model_predictions = predictions[
            predictions["model_name"] == model_name
        ].copy()

        plt.plot(
            model_predictions["date"],
            model_predictions["y_prob"],
            label=model_name,
            alpha=0.8,
        )

    plt.axhline(0.5, linestyle="--", linewidth=1)
    plt.title("Week 6 Walk-Forward Model Probabilities")
    plt.xlabel("Date")
    plt.ylabel("Predicted probability of positive next-day return")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def write_report(
    feature_file: Path,
    model_metrics: pd.DataFrame,
    backtest_metrics: pd.DataFrame,
    probability_plot_path: Path,
    output_path: Path,
) -> None:
    model_metrics_table = dataframe_to_markdown(model_metrics)
    backtest_metrics_table = dataframe_to_markdown(backtest_metrics)

    report = f"""# Week 6 Report: Walk-Forward Machine Learning

## Objective

The objective of this week was to add leakage-aware machine learning to the quant research pipeline.

The focus was not to maximise performance, but to evaluate simple ML models properly using walk-forward validation and transaction-cost-aware backtesting.

## Data

Feature file used:

`{feature_file}`

The feature dataset was created from the Week 2 data pipeline.

## Features Used

- 1-day return
- 1-day log return
- 5-day volatility
- 20-day volatility
- 1-day volume change
- distance from 5-day moving average
- distance from 20-day moving average

## Prediction Target

The prediction target is whether the next day's return is positive.

This is a binary classification problem:

- 1 = next return is positive
- 0 = next return is not positive

## Validation Method

I used walk-forward validation.

At each fold:

1. Train on all data available up to that point.
2. Predict on the next out-of-sample window.
3. Move forward in time.
4. Repeat.

This avoids random train/test splitting, which would leak future information in a time-series setting.

## Models Tested

- Logistic regression
- Random forest
- Histogram gradient boosting classifier

## Classification Results

{model_metrics_table}

## ML Signal Construction

Predicted probabilities were converted into trading signals:

- probability > 0.53: long
- probability < 0.47: short
- otherwise: flat

The neutral zone avoids trading on weak model confidence.

## ML Signal Backtest Results

{backtest_metrics_table}

## Probability Plot

See:

`{probability_plot_path}`

## Interpretation

The goal of this experiment is to test whether simple ML models add useful predictive information beyond basic baseline strategies.

The classification metrics should be interpreted carefully. A model can have accuracy above 50% and still fail as a trading strategy after costs. Conversely, a model with modest classification accuracy may still be useful if it performs well on high-confidence predictions and controls turnover.

The backtest results are therefore more important than raw accuracy.

## Key Lessons

- Random train/test splits are inappropriate for financial time series.
- Walk-forward validation is a better first validation method.
- Model probability outputs are more useful than hard class labels.
- Transaction costs can eliminate weak predictive signals.
- ML should be compared against simple baselines, not judged in isolation.
- A profitable-looking model is not credible unless it survives costs, turnover, and drawdown analysis.

## Limitations

- Features are still based on daily OHLCV data, not order-book data.
- The model target is simple next-day direction.
- The backtest is vectorised, not event-driven.
- Slippage and liquidity constraints are not yet modelled.
- Hyperparameters are basic and not optimised.
- The dataset is small for serious ML.
- The strategy uses fixed probability thresholds.

## Next Steps

- Add more assets.
- Add walk-forward hyperparameter tuning.
- Add calibration analysis.
- Compare ML signals against Week 5 baseline strategies.
- Add transaction cost sensitivity plots.
- Move toward intraday or order-book data.
"""

    output_path.write_text(report, encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    feature_file = find_feature_file()
    df = pd.read_parquet(feature_file)

    model_metrics, predictions = run_model_comparison(df)

    backtest_metrics = run_ml_signal_backtests(
        df=df,
        predictions=predictions,
        cost_bps_values=[0.0, 1.0, 5.0],
    )

    probability_plot_path = REPORTS_DIR / "week_6_model_probabilities.png"

    save_probability_plot(
        predictions=predictions,
        output_path=probability_plot_path,
    )

    report_path = REPORTS_DIR / "week_6_ml_results.md"

    write_report(
        feature_file=feature_file,
        model_metrics=model_metrics,
        backtest_metrics=backtest_metrics,
        probability_plot_path=probability_plot_path,
        output_path=report_path,
    )

    print("\nClassification metrics:")
    print(model_metrics.to_string(index=False))

    print("\nBacktest metrics:")
    print(backtest_metrics.to_string(index=False))

    print(f"\nSaved probability plot to {probability_plot_path}")
    print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()