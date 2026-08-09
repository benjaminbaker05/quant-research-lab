import pandas as pd

from src.reporting.strategy_report import compare_strategies


def test_compare_strategies_returns_all_baselines():
    df = pd.DataFrame(
        {
            "return_1d": [0.01, -0.02, 0.03, -0.01, 0.02] * 10,
            "volatility_20": [0.02] * 50,
            "close_to_ma_5": [0.01, -0.01, 0.02, -0.02, 0.0] * 10,
            "close_to_ma_20": [0.02, -0.02, 0.03, -0.03, 0.0] * 10,
            "future_return_1d": [0.01, 0.02, -0.01, 0.03, -0.02] * 10,
        }
    )

    comparison = compare_strategies(df)

    assert len(comparison) == 5
    assert "strategy" in comparison.columns
    assert "cumulative_return" in comparison.columns
    assert "sharpe_ratio" in comparison.columns
    assert "max_drawdown" in comparison.columns


def test_compare_strategies_is_sorted_by_sharpe():
    df = pd.DataFrame(
        {
            "return_1d": [0.01, -0.02, 0.03, -0.01, 0.02] * 10,
            "volatility_20": [0.02] * 50,
            "close_to_ma_5": [0.01, -0.01, 0.02, -0.02, 0.0] * 10,
            "close_to_ma_20": [0.02, -0.02, 0.03, -0.03, 0.0] * 10,
            "future_return_1d": [0.01, 0.02, -0.01, 0.03, -0.02] * 10,
        }
    )

    comparison = compare_strategies(df)

    sharpe_values = comparison["sharpe_ratio"].tolist()

    assert sharpe_values == sorted(sharpe_values, reverse=True)