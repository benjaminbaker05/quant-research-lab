# Quant Research Lab

A modular quantitative research platform for systematic trading research, financial modelling, backtesting, and market microstructure simulation.

The project combines **Python research infrastructure, statistical and machine-learning methods, derivatives pricing, portfolio/backtesting analytics, and C++ market-microstructure simulation** into a single reproducible research environment.

> **Status:** Core research pipeline complete. Automated test suite passing.

## Research Focus

The project investigates a set of related quantitative-finance problems:

* Can simple price and volatility features provide useful short-horizon predictive signals?
* How do baseline trading strategies behave under realistic backtesting assumptions?
* How should model performance be evaluated using time-aware validation rather than random train/test splits?
* How do transaction costs, turnover, volatility, and drawdowns affect strategy performance?
* How can classical derivatives models be implemented and tested from first principles?
* How can market-making and order-book behaviour be explored through simulation?

The emphasis is on **research methodology and reproducibility rather than claiming production-ready trading alpha**.

## Architecture

```text
Market Data
    |
    v
Data Cleaning
    |
    v
Feature Engineering
    |
    +--------------------> Statistical / ML Models
    |                              |
    |                              v
    |                       Walk-Forward Validation
    |                              |
    v                              v
Strategy Signals -----------> Backtesting
                                   |
                                   v
                            Risk & Performance
                                Metrics
                                   |
                                   v
                            Research Reports


Independent Research Modules
    +-- Options Pricing
    +-- Implied Volatility
    +-- Delta Hedging
    +-- Market-Making Simulation
    +-- Kelly Betting
    +-- Markov Chains
    +-- Poisson Arrivals
    +-- C++ Limit-Order-Book Engine
```

## Core Components

### 1. Market Data Pipeline

The data layer handles ingestion and cleaning of OHLCV market data before it enters the research pipeline.

Key objectives include:

* Consistent time-series structure
* Missing-data handling
* Validation of market-data fields
* Reproducible local datasets
* Parquet-based storage for efficient research workflows

### 2. Feature Engineering

The feature pipeline constructs time-series features used by predictive models and trading strategies.

Current features include:

* Daily returns
* Log returns
* 5-day and 20-day moving averages
* 5-day and 20-day volatility
* Daily volume changes
* Price distance from moving averages
* Next-period return
* Binary direction target

The feature pipeline also includes safeguards to prevent repeatedly processing already-generated feature datasets.

### 3. Trading Strategies

Several deliberately simple strategies are implemented as research baselines:

* Long-only
* Moving-average trend following
* Moving-average mean reversion
* Volatility breakout
* Short-term reversal

These strategies are intended as **benchmarks for the research framework**, not as claims of persistent market alpha.

### 4. Backtesting & Performance Analysis

The backtesting framework evaluates strategy returns and produces standard quantitative performance statistics.

Metrics include:

* Cumulative return
* Annualised return
* Annualised volatility
* Sharpe ratio
* Maximum drawdown
* Hit rate
* Average turnover

The project separates signal generation, portfolio returns, and performance measurement to make the framework easier to extend.

### 5. Machine Learning & Walk-Forward Validation

The ML component explores short-horizon return-direction prediction using engineered market features.

Rather than relying solely on random train/test splits, the project includes **walk-forward validation**, reflecting the temporal structure of financial data.

This helps reduce the risk of introducing look-ahead bias through inappropriate validation methodology.

The research treats predictive accuracy as only one part of model evaluation; trading performance, stability, turnover, and risk are also relevant.

### 6. Options & Volatility

The options module implements classical derivatives calculations, including:

* Black-Scholes pricing
* Implied volatility
* Option Greeks
* Delta hedging

The implementation provides a foundation for studying the relationship between theoretical pricing, volatility assumptions, and hedging behaviour.

### 7. Market Microstructure & Simulation

The project explores market microstructure and stochastic processes through simulation.

Included research modules cover:

* Limit-order-book simulation
* Market-making behaviour
* Order-arrival modelling
* Poisson processes
* Markov chains
* Kelly criterion / betting simulations

A C++ limit-order-book engine provides an additional performance-oriented component alongside the Python research stack.

## Testing

The project uses `pytest` for automated validation across the major research modules.

The test suite covers:

* Backtesting
* Data cleaning
* Feature engineering
* Options calculations
* Reporting
* Simulations
* Walk-forward validation

Current test status:

```text
27 passed
```

The objective is to ensure that quantitative calculations remain reproducible as the research code evolves.

## Project Structure

```text
quant-research-lab/
|
+-- src/
|   +-- backtest/
|   |   +-- metrics.py
|   |   +-- strategies.py
|   |   +-- vectorized.py
|   |
|   +-- data/
|   |   +-- clean.py
|   |   +-- download.py
|   |
|   +-- features/
|   |   +-- build_features.py
|   |
|   +-- models/
|   |   +-- baseline.py
|   |   +-- walk_forward.py
|   |   +-- run_ml_experiment.py
|   |
|   +-- options/
|   |   +-- black_scholes.py
|   |   +-- implied_vol.py
|   |   +-- delta_hedging.py
|   |   +-- run_options_experiment.py
|   |
|   +-- reporting/
|   |   +-- strategy_report.py
|   |
|   +-- simulations/
|       +-- coin_market_making.py
|       +-- kelly_betting.py
|       +-- markov_chain.py
|       +-- poisson_arrivals.py
|
+-- tests/
|   +-- test_backtest.py
|   +-- test_data_cleaning.py
|   +-- test_features.py
|   +-- test_options.py
|   +-- test_reporting.py
|   +-- test_simulations.py
|   +-- test_walk_forward.py
|
+-- reports/
+-- docs/
+-- pyproject.toml
```

## Reproducibility

Create and activate the virtual environment, install the project dependencies, and run the test suite:

```bash
pytest
```

Expected result:

```text
27 passed
```

The research modules can then be run individually to reproduce feature generation, model experiments, backtests, options experiments, simulations, and reporting outputs.

## Research Philosophy

This project deliberately focuses on **robust research infrastructure rather than overfitting a single strategy**.

Important principles include:

1. **Simple baselines first**

   Complex models should demonstrate value relative to interpretable benchmarks.

2. **Time-aware validation**

   Financial observations are temporally ordered, so validation methodology must respect that structure.

3. **Risk matters alongside return**

   Sharpe ratio, volatility, drawdown, and turnover provide more information than raw cumulative returns alone.

4. **Reproducibility matters**

   Quantitative results should be generated from code rather than manually assembled analyses.

5. **No unsupported alpha claims**

   Backtested performance is not evidence of future profitability, particularly without extensive out-of-sample and transaction-cost analysis.

## Research Report

A detailed project report is available at:

```text
reports/final_research_report_v1.md
```

The report covers:

* Project architecture
* Data pipeline
* Feature engineering
* Machine-learning methodology
* Walk-forward validation
* Strategy backtesting
* Probability simulations
* Market microstructure
* Options modelling
* Limitations
* Future research directions

## Limitations & Future Work

The current platform is a research environment rather than a production trading system.

Potential future extensions include:

* Richer transaction-cost models
* Slippage and liquidity modelling
* Portfolio-level risk management
* Additional cross-sectional features
* Alternative ML models
* Larger multi-asset datasets
* Event-driven backtesting
* More realistic order-book dynamics
* Stronger out-of-sample evaluation
* Live/paper-trading integration

The most important next step for any claimed strategy would be demonstrating robustness across different assets, time periods, market regimes, and realistic execution assumptions.

## Disclaimer

This repository is an educational and research project.

Backtested or simulated results do not guarantee future performance. Nothing in this repository constitutes investment advice or a recommendation to trade any financial instrument.
