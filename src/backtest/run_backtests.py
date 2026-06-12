from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.backtest.strategies import add_strategy_signals
from src.backtest.vectorized import run_vectorized_backtest


PROCESSED_DATA_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")

STRATEGY_COLUMNS = [
    "signal_long_only",
    "signal_trend_ma_20",
    "signal_mean_reversion_ma_20",
    "signal_volatility_breakout",
    "signal_short_term_reversal",
]


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert a DataFrame to a simple markdown table without requiring tabulate.
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


def run_all_backtests(
    feature_file: Path,
    cost_bps_values: list[float],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    df = pd.read_parquet(feature_file)
    df = add_strategy_signals(df)

    summary_rows = []
    equity_curves = {}

    for cost_bps in cost_bps_values:
        for strategy in STRATEGY_COLUMNS:
            result = run_vectorized_backtest(
                df=df,
                signal_column=strategy,
                cost_bps=cost_bps,
            )

            row = {
                "strategy": strategy,
                "cost_bps": cost_bps,
                "cumulative_return": round(result.metrics["cumulative_return"], 4),
                "annualised_return": round(result.metrics["annualised_return"], 4),
                "annualised_volatility": round(
                    result.metrics["annualised_volatility"],
                    4,
                ),
                "sharpe_ratio": round(result.metrics["sharpe_ratio"], 4),
                "max_drawdown": round(result.metrics["max_drawdown"], 4),
                "hit_rate": round(result.metrics["hit_rate"], 4),
                "average_turnover": round(result.metrics["average_turnover"], 4),
            }

            summary_rows.append(row)

            if cost_bps == 1.0:
                equity_curves[strategy] = result.results[
                    ["date", "equity_curve"]
                ].copy()

    summary = pd.DataFrame(summary_rows)

    return summary, equity_curves


def save_equity_curve_plot(
    equity_curves: dict[str, pd.DataFrame],
    output_path: Path,
) -> None:
    plt.figure(figsize=(10, 6))

    for strategy, curve in equity_curves.items():
        plt.plot(
            pd.to_datetime(curve["date"]),
            curve["equity_curve"],
            label=strategy,
        )

    plt.title("Week 5 Strategy Equity Curves, 1bp Cost")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def write_report(
    summary: pd.DataFrame,
    feature_file: Path,
    plot_path: Path,
    output_path: Path,
) -> None:
    markdown_table = dataframe_to_markdown(summary)

    report = f"""# Week 5 Report: Baseline Strategy Backtesting

## Objective

The objective of this week was to build a simple vectorised backtesting engine and evaluate baseline trading strategies after transaction costs.

## Data

Feature file used:

`{feature_file}`

The strategy signals use the feature dataset created in Week 2.

## Strategies Tested

- Long-only benchmark
- 20-day moving-average trend-following
- 20-day moving-average mean reversion
- Volatility breakout
- Short-term reversal

## Transaction Cost Assumptions

The backtester was run with three cost levels:

- 0 bps
- 1 bp
- 5 bps

Costs are charged on turnover:

`cost = abs(position_t - position_t_minus_1) * cost_bps / 10_000`

## Results

{markdown_table}

## Equity Curves

See:

`{plot_path}`

## Interpretation

These are baseline strategies, not final trading strategies. The purpose of this stage is to test the research infrastructure and understand how returns, turnover, drawdowns, and transaction costs interact.

## Key Lessons

- A strategy must be evaluated after transaction costs.
- Turnover matters because frequent position changes increase costs.
- Accuracy alone is not enough; drawdown, volatility, and Sharpe ratio matter.
- Simple baselines are essential before adding more advanced machine learning.

## Limitations

- Uses daily OHLCV-derived features, not order-book data.
- Uses a simple vectorised backtest, not an event-driven execution simulator.
- Does not model slippage or liquidity constraints.
- Does not yet include walk-forward model training.
- Does not yet connect to the C++ limit-order-book engine.

## Next Steps

- Add walk-forward validation.
- Add ML-generated trading signals.
- Compare ML signals against simple baselines.
- Add slippage assumptions.
- Move toward event-driven backtesting.
"""

    output_path.write_text(report, encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    feature_file = find_feature_file()

    summary, equity_curves = run_all_backtests(
        feature_file=feature_file,
        cost_bps_values=[0.0, 1.0, 5.0],
    )

    print(summary.to_string(index=False))

    plot_path = REPORTS_DIR / "week_5_equity_curves.png"
    save_equity_curve_plot(
        equity_curves=equity_curves,
        output_path=plot_path,
    )

    report_path = REPORTS_DIR / "week_5_backtest_results.md"
    write_report(
        summary=summary,
        feature_file=feature_file,
        plot_path=plot_path,
        output_path=report_path,
    )

    print(f"\nSaved plot to {plot_path}")
    print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()