\# A Reproducible Python/C++ Research Pipeline for Financial Time-Series Modelling, Backtesting, and Market Microstructure Simulation



\## Abstract



This project develops a reproducible quantitative research pipeline combining Python-based financial time-series modelling, machine learning, strategy backtesting, probability simulations, mathematical finance, and a C++ limit-order-book engine.



The objective is not to claim a production-ready trading strategy, but to demonstrate a structured research workflow: data ingestion, feature engineering, baseline modelling, leakage-aware validation, transaction-cost-aware backtesting, options pricing, risk simulation, and performance-aware systems engineering.



The project currently includes:



\- OHLCV data ingestion and cleaning

\- time-series feature engineering

\- baseline classification models

\- walk-forward machine learning validation

\- transaction-cost-aware vectorised backtesting

\- probability and market-making simulations

\- C++ limit-order-book implementation

\- Black-Scholes pricing, Greeks, implied volatility, and delta hedging

\- pytest coverage and research reports



\## 1. Research Motivation



Quantitative finance requires more than building predictive models. A useful research process must address data quality, feature design, model validation, transaction costs, risk, reproducibility, and implementation constraints.



This project was designed to answer the following question:



Can I build a credible end-to-end quant research framework that connects market data, statistical modelling, backtesting, probability, derivatives mathematics, and systems engineering?



The project focuses on process quality rather than overclaiming alpha.



\## 2. Project Architecture



The project is organised into several modules:



```text

src/

&#x20; data/

&#x20; features/

&#x20; models/

&#x20; backtest/

&#x20; simulations/

&#x20; options/

&#x20; reporting/



cpp/

&#x20; include/

&#x20; src/

&#x20; tests/

&#x20; benchmarks/



tests/

reports/



The Python modules support data processing, modelling, backtesting, simulations, options pricing, and reporting.



The C++ module implements a simplified limit-order-book engine with price-time priority.



\## 3. Data Pipeline



The data pipeline downloads daily OHLCV market data, cleans it, standardises column names, handles missing values, sorts observations by date, and saves processed data in Parquet format.



The current data source is intentionally simple. Daily OHLCV data is sufficient for building and validating the research framework, but it is not detailed enough for true market microstructure research.



The pipeline follows this structure:



raw market data

\- cleaned data

\- feature dataset

\- model inputs

\- backtest inputs



\## 4. Feature Engineering



The feature set currently includes:



1-day return

1-day log return

5-day moving average

20-day moving average

5-day volatility

20-day volatility

volume change

distance from 5-day moving average

distance from 20-day moving average



The prediction target is whether the next day's return is positive.



This target is deliberately simple. It allows the research framework to test model validation and backtesting logic before moving to richer intraday or order-book data.



\## 5. Exploratory Data Analysis



The project generates basic exploratory figures:



These plots help identify the behaviour of returns and relationships among engineered features.



\## 6. Baseline Modelling



The first modelling step uses logistic regression to predict next-day return direction.



This baseline is important because complex models should only be introduced after simple models have been tested. A simple baseline provides a reference point for evaluating whether more advanced machine learning adds value.



\## 7. Walk-Forward Machine Learning



Financial time series must be validated carefully because random train/test splits can leak future information.



The project therefore implements walk-forward validation:



train on past data

→ predict future window

→ move forward

→ repeat



Models compared include:



logistic regression

random forest classifier

histogram gradient boosting classifier



The output is a set of out-of-sample predicted probabilities.



These probabilities are converted into trading signals using thresholds:



probability > 0.53: long

probability < 0.47: short

otherwise: flat



The neutral zone avoids trading on weak model confidence.



\## 8. Backtesting Framework



The project includes a vectorised backtesting engine that calculates:



position

turnover

transaction costs

gross strategy returns

net strategy returns

equity curve

cumulative return

annualised return

annualised volatility

Sharpe ratio

max drawdown

hit rate



The backtester compares simple baseline strategies:



long-only benchmark

moving-average trend-following

moving-average mean reversion

volatility breakout

short-term reversal



It also evaluates ML-generated signals after costs.



Transaction costs are modelled as:



cost = abs(position\_t - position\_t\_minus\_1) × cost\_bps / 10,000



This is simplified, but it forces the research process to account for turnover and cost sensitivity.



\## 9. Probability and Market-Making Simulations



The project includes probability simulations covering:



expected value

market-making spread capture

toxic informed flow

Poisson order arrivals

Markov chain regime transitions

Kelly betting and position sizing



The market-making simulation illustrates a key idea:



A market maker may earn spread from uninformed flow, but informed flow can create adverse selection and damage expected P\&L.



This helps connect probability theory to trading intuition.



\## 10. C++ Limit Order Book



The C++ module implements a simplified limit order book supporting:



limit buy orders

limit sell orders

market buy orders

market sell orders

order cancellation

best bid

best ask

price-time priority

FIFO matching at each price level

simple benchmarking



This module demonstrates systems programming and market microstructure understanding.



The current implementation is educational rather than production-grade. In particular, cancellation currently scans the book rather than using an order-location map.



\## 11. Options and Mathematical Finance



The project includes an options module implementing:



Black-Scholes European call pricing

Black-Scholes European put pricing

Greeks: delta, gamma, vega, theta, rho

implied volatility estimation by binary search

geometric Brownian motion simulation

delta hedging simulation



The delta hedging experiment demonstrates that option P\&L depends on more than direction. A delta-hedged option position remains exposed to realised volatility, gamma, discrete hedging error, and model assumptions.



\## 12. Results Summary



The most important result of this project so far is not a specific trading strategy. The main result is the construction of a reproducible research framework.



The framework can:



ingest data

create features

train baseline and ML models

avoid random time-series leakage

convert probabilities into trading signals

evaluate strategies after transaction costs

calculate risk metrics

simulate probability and market-making concepts

price and hedge options

demonstrate C++ order-book mechanics



The current strategies and models should be interpreted as baseline experiments rather than evidence of production-ready alpha.

## Quantitative Results

## Backtest Results:

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

## Delta Hedging

The delta hedging simulation sells one call option and dynamically hedges using the underlying asset.

The experiment compares scenarios where realised volatility is below, equal to, or above implied volatility.

| scenario | implied_volatility | realised_volatility | final_pnl | max_abs_hedge | hedge_turnover |
| --- | --- | --- | --- | --- | --- |
| realised_vol_below_implied | 0.25 | 0.15 | 5.3219 | 0.664 | 4.6005 |
| realised_vol_equal_implied | 0.25 | 0.25 | 1.4941 | 0.7122 | 5.6102 |
| realised_vol_above_implied | 0.25 | 0.4 | -2.4305 | 0.7725 | 5.5964 |

The baseline strategy results show that transaction costs materially affect performance, particularly for higher-turnover strategies.

The walk-forward ML results show that classification accuracy alone is insufficient. The more important test is whether out-of-sample probabilities produce useful trading signals after costs.

The options experiments show that Black-Scholes pricing and delta hedging are sensitive to volatility assumptions. The delta hedging simulation highlights the gap between implied and realised volatility.

\## 13. Limitations



The current project has several limitations:



data is daily OHLCV rather than intraday or order-book data

transaction costs are simplified

slippage and liquidity constraints are not yet modelled

the backtester is vectorised rather than event-driven

ML features are basic

hyperparameters are not deeply tuned

options module assumes Black-Scholes conditions

C++ order book is simplified

no live trading or production deployment is attempted



These limitations are intentional and documented because overclaiming would make the project less credible.



\## 14. Future Work



The next stages are:



Add walk-forward hyperparameter tuning.

Add richer multi-asset datasets.

Add transaction cost sensitivity plots.

Add event-driven backtesting.

Connect the Python research layer to the C++ order book.

Add Python bindings for the C++ engine.

Add order-book or intraday market data.

Improve C++ cancellation performance using an order-location map.

Add option hedging transaction costs.

Produce a polished PDF research report.



\## 15. Conclusion



This project demonstrates an end-to-end quantitative research workflow across data engineering, machine learning, backtesting, probability, market microstructure, options mathematics, and C++ systems programming.



The strongest aspect of the project is its research discipline: simple baselines, leakage-aware validation, transaction-cost-aware evaluation, tests, reports, and clear limitations.



The project should be viewed as a serious research framework under development rather than a finished trading system.

