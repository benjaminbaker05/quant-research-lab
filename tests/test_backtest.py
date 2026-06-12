import pandas as pd
import pytest

from src.backtest.metrics import calculate_max_drawdown
from src.backtest.strategies import add_strategy_signals
from src.backtest.vectorized import run_vectorized_backtest


def test_vectorized_backtest_creates_equity_curve():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5),
            "signal": [1, 1, 1, 1, 1],
            "future_return_1d": [0.01, -0.01, 0.02, 0.0, 0.01],
        }
    )

    result = run_vectorized_backtest(
        df=df,
        signal_column="signal",
        cost_bps=0.0,
    )

    assert "equity_curve" in result.results.columns
    assert "strategy_return" in result.results.columns
    assert result.results["equity_curve"].iloc[-1] > 0


def test_transaction_costs_reduce_returns():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5),
            "signal": [1, -1, 1, -1, 1],
            "future_return_1d": [0.01, 0.01, 0.01, 0.01, 0.01],
        }
    )

    no_cost = run_vectorized_backtest(
        df=df,
        signal_column="signal",
        cost_bps=0.0,
    )

    with_cost = run_vectorized_backtest(
        df=df,
        signal_column="signal",
        cost_bps=10.0,
    )

    assert (
        with_cost.metrics["cumulative_return"]
        < no_cost.metrics["cumulative_return"]
    )


def test_strategy_signals_are_added():
    df = pd.DataFrame(
        {
            "return_1d": [0.01, -0.02, 0.03],
            "volatility_20": [0.01, 0.01, 0.01],
            "close_to_ma_5": [0.01, -0.01, 0.0],
            "close_to_ma_20": [0.02, -0.02, 0.0],
        }
    )

    output = add_strategy_signals(df)

    assert "signal_long_only" in output.columns
    assert "signal_trend_ma_20" in output.columns
    assert "signal_mean_reversion_ma_20" in output.columns
    assert "signal_volatility_breakout" in output.columns
    assert "signal_short_term_reversal" in output.columns


def test_max_drawdown_is_negative_or_zero():
    equity_curve = pd.Series([1.0, 1.1, 1.05, 1.2, 0.9])

    max_drawdown = calculate_max_drawdown(equity_curve)

    assert max_drawdown <= 0
    assert max_drawdown == pytest.approx(-0.25)