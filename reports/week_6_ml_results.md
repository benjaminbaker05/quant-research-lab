# Week 6 Report: Walk-Forward Machine Learning

## Objective

The objective of this week was to add leakage-aware machine learning to the quant research pipeline.

The focus was not to maximise performance, but to evaluate simple ML models properly using walk-forward validation and transaction-cost-aware backtesting.

## Data

Feature file used:

`data\processed\features_features_features_SPY_1d_2020-01-01_2025-01-01.parquet`

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
| logistic_regression | 0.5338 | 0.5372 | 0.9652 | 0.6902 | 0.4666 | 695 |
| random_forest | 0.5281 | 0.5381 | 0.869 | 0.6646 | 0.4894 | 695 |
| hist_gradient_boosting | 0.4993 | 0.5275 | 0.6658 | 0.5887 | 0.4835 | 695 |

## ML Signal Construction

Predicted probabilities were converted into trading signals:

- probability > 0.53: long
- probability < 0.47: short
- otherwise: flat

The neutral zone avoids trading on weak model confidence.

## ML Signal Backtest Results

| model | cost_bps | cumulative_return | annualised_return | annualised_volatility | sharpe_ratio | max_drawdown | hit_rate | average_turnover |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting | 0.0 | -0.1229 | -0.0464 | 0.1589 | -0.2922 | -0.312 | 0.436 | 0.7928 |
| hist_gradient_boosting | 1.0 | -0.1699 | -0.0653 | 0.1589 | -0.4109 | -0.3226 | 0.4317 | 0.7928 |
| hist_gradient_boosting | 5.0 | -0.3343 | -0.1372 | 0.1593 | -0.8613 | -0.3869 | 0.4216 | 0.7928 |
| logistic_regression | 0.0 | 0.1286 | 0.0448 | 0.1541 | 0.2908 | -0.1868 | 0.423 | 0.2173 |
| logistic_regression | 1.0 | 0.1116 | 0.0391 | 0.1541 | 0.2538 | -0.1875 | 0.4216 | 0.2173 |
| logistic_regression | 5.0 | 0.0465 | 0.0166 | 0.1542 | 0.1077 | -0.1901 | 0.4173 | 0.2173 |
| random_forest | 0.0 | 0.3365 | 0.1109 | 0.1591 | 0.6972 | -0.2139 | 0.4446 | 0.4475 |
| random_forest | 1.0 | 0.2956 | 0.0984 | 0.1591 | 0.6187 | -0.2186 | 0.4446 | 0.4475 |
| random_forest | 5.0 | 0.144 | 0.05 | 0.1593 | 0.3136 | -0.2372 | 0.4345 | 0.4475 |

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
