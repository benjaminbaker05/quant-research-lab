from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_cumulative_return(returns: pd.Series) -> float:
    """
    Calculate total cumulative return from a series of periodic returns.
    """
    returns = returns.fillna(0.0)

    if returns.empty:
        return 0.0

    return float((1.0 + returns).prod() - 1.0)


def calculate_annualised_return(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Calculate annualised return.
    """
    returns = returns.fillna(0.0)

    if returns.empty:
        return 0.0

    cumulative_return = (1.0 + returns).prod()
    n_periods = len(returns)

    if n_periods == 0:
        return 0.0

    return float(cumulative_return ** (periods_per_year / n_periods) - 1.0)


def calculate_annualised_volatility(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Calculate annualised volatility.
    """
    returns = returns.fillna(0.0)

    if returns.empty:
        return 0.0

    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))


def calculate_sharpe_ratio(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Calculate annualised Sharpe ratio assuming zero risk-free rate.
    """
    returns = returns.fillna(0.0)

    if returns.empty:
        return 0.0

    volatility = calculate_annualised_volatility(
        returns,
        periods_per_year=periods_per_year,
    )

    if volatility == 0:
        return 0.0

    annualised_return = calculate_annualised_return(
        returns,
        periods_per_year=periods_per_year,
    )

    return float(annualised_return / volatility)


def calculate_max_drawdown(equity_curve: pd.Series) -> float:
    """
    Calculate maximum drawdown from an equity curve.
    """
    equity_curve = equity_curve.dropna()

    if equity_curve.empty:
        return 0.0

    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1.0

    return float(drawdown.min())


def calculate_hit_rate(returns: pd.Series) -> float:
    """
    Percentage of periods with positive strategy returns.
    """
    returns = returns.dropna()

    if returns.empty:
        return 0.0

    return float((returns > 0).mean())


def calculate_metrics(
    strategy_returns: pd.Series,
    equity_curve: pd.Series,
    turnover: pd.Series,
) -> dict[str, float]:
    """
    Calculate standard backtest metrics.
    """
    strategy_returns = strategy_returns.fillna(0.0)
    turnover = turnover.fillna(0.0)

    return {
        "cumulative_return": calculate_cumulative_return(strategy_returns),
        "annualised_return": calculate_annualised_return(strategy_returns),
        "annualised_volatility": calculate_annualised_volatility(strategy_returns),
        "sharpe_ratio": calculate_sharpe_ratio(strategy_returns),
        "max_drawdown": calculate_max_drawdown(equity_curve),
        "hit_rate": calculate_hit_rate(strategy_returns),
        "average_turnover": float(turnover.mean()) if not turnover.empty else 0.0,
    }