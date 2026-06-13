# Week 5 Report: Baseline Strategy Backtesting

## Objective

The objective of this week was to build a simple vectorised backtesting engine and evaluate baseline trading strategies after transaction costs.

## Data

Feature file used:

`data\processed\features_features_features_features_SPY_1d_2020-01-01_2025-01-01.parquet`

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

| strategy | cost_bps | cumulative_return | annualised_return | annualised_volatility | sharpe_ratio | max_drawdown | hit_rate | average_turnover |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| signal_long_only | 0.0 | 1.2567 | 0.1909 | 0.1691 | 1.1291 | -0.245 | 0.5511 | 0.0009 |
| signal_trend_ma_20 | 0.0 | 0.0545 | 0.0115 | 0.1695 | 0.0676 | -0.2422 | 0.5375 | 0.1882 |
| signal_mean_reversion_ma_20 | 0.0 | 0.0407 | 0.0086 | 0.1409 | 0.061 | -0.1963 | 0.3501 | 0.2232 |
| signal_volatility_breakout | 0.0 | 0.1455 | 0.0296 | 0.0984 | 0.3007 | -0.1388 | 0.1712 | 0.5426 |
| signal_short_term_reversal | 0.0 | -0.078 | -0.0173 | 0.1693 | -0.102 | -0.2489 | 0.4957 | 0.9957 |
| signal_long_only | 1.0 | 1.2565 | 0.1909 | 0.1691 | 1.1289 | -0.245 | 0.5511 | 0.0009 |
| signal_trend_ma_20 | 1.0 | 0.0315 | 0.0067 | 0.1695 | 0.0394 | -0.2466 | 0.5366 | 0.1882 |
| signal_mean_reversion_ma_20 | 1.0 | 0.0137 | 0.0029 | 0.1409 | 0.0208 | -0.2062 | 0.3484 | 0.2232 |
| signal_volatility_breakout | 1.0 | 0.0749 | 0.0156 | 0.0984 | 0.1587 | -0.1561 | 0.1704 | 0.5426 |
| signal_short_term_reversal | 1.0 | -0.1797 | -0.0416 | 0.1693 | -0.2459 | -0.2714 | 0.4923 | 0.9957 |
| signal_long_only | 5.0 | 1.2556 | 0.1908 | 0.1691 | 1.1284 | -0.245 | 0.5511 | 0.0009 |
| signal_trend_ma_20 | 5.0 | -0.0558 | -0.0122 | 0.1694 | -0.0722 | -0.2779 | 0.5315 | 0.1882 |
| signal_mean_reversion_ma_20 | 5.0 | -0.0872 | -0.0194 | 0.141 | -0.1375 | -0.2447 | 0.345 | 0.2232 |
| signal_volatility_breakout | 5.0 | -0.1669 | -0.0384 | 0.0984 | -0.3907 | -0.2447 | 0.1644 | 0.5426 |
| signal_short_term_reversal | 5.0 | -0.4863 | -0.1332 | 0.1696 | -0.7855 | -0.5033 | 0.4668 | 0.9957 |

## Equity Curves

See:

`reports\week_5_equity_curves.png`

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
