from __future__ import annotations

import pandas as pd

from src.backtest.strategies import add_strategy_signals
from src.backtest.vectorized import run_vectorized_backtest


STRATEGY_COLUMNS = [
    "signal_long_only",
    "signal_trend_ma_20",
    "signal_mean_reversion_ma_20",
    "signal_volatility_breakout",
    "signal_short_term_reversal",
]


def compare_strategies(
    df: pd.DataFrame,
    cost_bps: float = 1.0,
) -> pd.DataFrame:
    """
    Run all baseline strategies and return a comparison table.
    """
    data = add_strategy_signals(df)

    rows = []

    for signal_column in STRATEGY_COLUMNS:
        result = run_vectorized_backtest(
            df=data,
            signal_column=signal_column,
            return_column="future_return_1d",
            cost_bps=cost_bps,
        )

        metrics = result.metrics

        rows.append(
            {
                "strategy": signal_column,
                "cumulative_return": metrics["cumulative_return"],
                "annualised_return": metrics["annualised_return"],
                "annualised_volatility": metrics["annualised_volatility"],
                "sharpe_ratio": metrics["sharpe_ratio"],
                "max_drawdown": metrics["max_drawdown"],
                "hit_rate": metrics["hit_rate"],
                "average_turnover": metrics["average_turnover"],
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values("sharpe_ratio", ascending=False)
        .reset_index(drop=True)
    )