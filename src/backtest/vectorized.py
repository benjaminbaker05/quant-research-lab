from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.backtest.metrics import calculate_metrics


@dataclass
class BacktestResult:
    strategy_name: str
    cost_bps: float
    results: pd.DataFrame
    metrics: dict[str, float]


def run_vectorized_backtest(
    df: pd.DataFrame,
    signal_column: str,
    return_column: str = "future_return_1d",
    cost_bps: float = 1.0,
    initial_equity: float = 1.0,
) -> BacktestResult:
    """
    Run a simple vectorised backtest.

    The signal at time t is applied to the future return from t to t+1.

    Transaction costs are charged on turnover:
    cost = abs(position_t - position_{t-1}) * cost_bps / 10_000
    """
    if signal_column not in df.columns:
        raise ValueError(f"Signal column not found: {signal_column}")

    if return_column not in df.columns:
        raise ValueError(f"Return column not found: {return_column}")

    if cost_bps < 0:
        raise ValueError("cost_bps must be non-negative")

    if initial_equity <= 0:
        raise ValueError("initial_equity must be positive")

    results = df.copy()

    results["position"] = results[signal_column].astype(float)

    results["previous_position"] = results["position"].shift(1).fillna(0.0)
    results["turnover"] = (
        results["position"] - results["previous_position"]
    ).abs()

    results["transaction_cost"] = results["turnover"] * cost_bps / 10_000

    results["gross_strategy_return"] = (
        results["position"] * results[return_column]
    )

    results["strategy_return"] = (
        results["gross_strategy_return"] - results["transaction_cost"]
    )

    results["equity_curve"] = (
        initial_equity * (1.0 + results["strategy_return"]).cumprod()
    )

    metrics = calculate_metrics(
        strategy_returns=results["strategy_return"],
        equity_curve=results["equity_curve"],
        turnover=results["turnover"],
    )

    return BacktestResult(
        strategy_name=signal_column,
        cost_bps=cost_bps,
        results=results,
        metrics=metrics,
    )