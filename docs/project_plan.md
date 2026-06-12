# Project Plan

## Research Question

Can short-horizon price movement or volatility be predicted from simple market microstructure features such as order-book imbalance, spread, recent returns, and trade intensity?

## Hypotheses

1. Order-book imbalance contains weak predictive information for very short-horizon returns.
2. Predictive signals decay quickly after transaction costs.
3. Simple models may outperform complex ML models once leakage and costs are controlled.
4. Market-making profitability depends more on spread, fill probability, inventory risk, and adverse selection than raw directional accuracy.

## Data

Initial data source: crypto order-book/trade data or other publicly available high-frequency market data.

## Models

- Logistic regression
- Linear regression
- Random forest
- Gradient boosting
- Simple neural network only if justified

## Evaluation

- Walk-forward validation
- Baseline comparison
- Transaction-cost-aware backtesting
- Sharpe ratio
- Drawdown
- Hit rate
- Turnover
- Model calibration
- Feature importance

## Engineering Components

- Python research pipeline
- C++ limit-order-book simulator
- Unit tests
- CI
- Reproducible reports