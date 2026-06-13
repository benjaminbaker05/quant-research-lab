# Week 6 Report: Walk-Forward Machine Learning

## Objective

The objective of this week was to add leakage-aware machine learning to the quant research pipeline.

The focus was not to maximise performance, but to evaluate simple ML models properly using walk-forward validation and transaction-cost-aware backtesting.

## Data

Feature file used:

`data\processed\features_features_features_features_SPY_1d_2020-01-01_2025-01-01.parquet`

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

| model | accuracy | precision | recall | f1 | roc_auc | n_predictions |
| --- | --- | --- | --- | --- | --- | --- |
| logistic_regression | 0.546 | 0.5457 | 0.9505 | 0.6934 | 0.4755 | 674 |
| random_forest | 0.5163 | 0.5335 | 0.8324 | 0.6502 | 0.4769 | 674 |
| hist_gradient_boosting | 0.4926 | 0.5233 | 0.6786 | 0.5909 | 0.4711 | 674 |

## ML Signal Construction

Predicted probabilities were converted into trading signals:

- probability > 0.53: long
- probability < 0.47: short
- otherwise: flat

The neutral zone avoids trading on weak model confidence.

## ML Signal Backtest Results

| model | cost_bps | cumulative_return | annualised_return | annualised_volatility | sharpe_ratio | max_drawdown | hit_rate | average_turnover |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting | 0.0 | -0.3429 | -0.1453 | 0.1637 | -0.8877 | -0.4178 | 0.4243 | 0.7226 |
| hist_gradient_boosting | 1.0 | -0.3742 | -0.1607 | 0.1638 | -0.9816 | -0.4377 | 0.4228 | 0.7226 |
| hist_gradient_boosting | 5.0 | -0.4851 | -0.2198 | 0.1642 | -1.3386 | -0.5199 | 0.4125 | 0.7226 |
| logistic_regression | 0.0 | 0.289 | 0.0996 | 0.1522 | 0.6541 | -0.1498 | 0.4525 | 0.1528 |
| logistic_regression | 1.0 | 0.2758 | 0.0954 | 0.1522 | 0.6263 | -0.1507 | 0.4496 | 0.1528 |
| logistic_regression | 5.0 | 0.2244 | 0.0786 | 0.1522 | 0.5164 | -0.1611 | 0.4496 | 0.1528 |
| random_forest | 0.0 | 0.1042 | 0.0378 | 0.1508 | 0.2504 | -0.2114 | 0.4318 | 0.4228 |
| random_forest | 1.0 | 0.0732 | 0.0268 | 0.1508 | 0.1774 | -0.2223 | 0.4318 | 0.4228 |
| random_forest | 5.0 | -0.0425 | -0.0161 | 0.151 | -0.1067 | -0.2645 | 0.4273 | 0.4228 |

## Probability Plot

See:

`reports\week_6_model_probabilities.png`

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
