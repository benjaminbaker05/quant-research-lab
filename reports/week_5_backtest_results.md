# Week 5 Report: Baseline Strategy Backtesting

## Objective

The objective of this week was to build a simple vectorised backtesting engine and evaluate baseline trading strategies after transaction costs.

## Data

Feature file used:

`data\processed\features_features_SPY_1d_2020-01-01_2025-01-01.parquet`

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
| signal_long_only | 0.0 | 1.0527 | 0.1607 | 0.2096 | 0.7666 | -0.2832 | 0.5485 | 0.0008 |
| signal_trend_ma_20 | 0.0 | 0.2278 | 0.0434 | 0.2099 | 0.207 | -0.2422 | 0.5387 | 0.185 |
| signal_mean_reversion_ma_20 | 0.0 | -0.1083 | -0.0235 | 0.1869 | -0.1256 | -0.2832 | 0.352 | 0.2204 |
| signal_volatility_breakout | 0.0 | -0.2218 | -0.0506 | 0.1354 | -0.374 | -0.4012 | 0.1694 | 0.5452 |
| signal_short_term_reversal | 0.0 | 0.4449 | 0.0793 | 0.2097 | 0.378 | -0.2489 | 0.5016 | 1.0074 |
| signal_long_only | 1.0 | 1.0524 | 0.1607 | 0.2096 | 0.7665 | -0.2832 | 0.5485 | 0.0008 |
| signal_trend_ma_20 | 1.0 | 0.2005 | 0.0386 | 0.2099 | 0.1839 | -0.2466 | 0.5378 | 0.185 |
| signal_mean_reversion_ma_20 | 1.0 | -0.1319 | -0.0289 | 0.1869 | -0.1545 | -0.2832 | 0.3503 | 0.2204 |
| signal_volatility_breakout | 1.0 | -0.2717 | -0.0636 | 0.1354 | -0.4697 | -0.4149 | 0.1686 | 0.5452 |
| signal_short_term_reversal | 1.0 | 0.2783 | 0.0522 | 0.2097 | 0.249 | -0.2723 | 0.4975 | 1.0074 |
| signal_long_only | 5.0 | 1.0516 | 0.1606 | 0.2097 | 0.7659 | -0.2832 | 0.5485 | 0.0008 |
| signal_trend_ma_20 | 5.0 | 0.0972 | 0.0194 | 0.2098 | 0.0925 | -0.2779 | 0.5329 | 0.185 |
| signal_mean_reversion_ma_20 | 5.0 | -0.2201 | -0.0502 | 0.187 | -0.2686 | -0.2922 | 0.347 | 0.2204 |
| signal_volatility_breakout | 5.0 | -0.4415 | -0.1137 | 0.1356 | -0.8387 | -0.4824 | 0.1628 | 0.5452 |
| signal_short_term_reversal | 5.0 | -0.217 | -0.0494 | 0.2099 | -0.2356 | -0.5043 | 0.4729 | 1.0074 |

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
