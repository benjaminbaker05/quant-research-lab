from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.options.black_scholes import (
    OptionInputs,
    black_scholes_call_price,
    call_greeks,
)


TRADING_DAYS_PER_YEAR = 252


@dataclass
class DeltaHedgeResult:
    path: pd.DataFrame
    final_pnl: float
    max_abs_hedge: float
    hedge_turnover: float


def simulate_gbm_price_path(
    spot: float = 100.0,
    drift: float = 0.0,
    volatility: float = 0.20,
    n_steps: int = 252,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Simulate a geometric Brownian motion price path.
    """
    if spot <= 0:
        raise ValueError("spot must be positive")

    if volatility <= 0:
        raise ValueError("volatility must be positive")

    if n_steps <= 0:
        raise ValueError("n_steps must be positive")

    rng = np.random.default_rng(seed)

    dt = 1.0 / TRADING_DAYS_PER_YEAR
    shocks = rng.normal(0.0, 1.0, size=n_steps)

    prices = [spot]

    for shock in shocks:
        previous_price = prices[-1]

        next_price = previous_price * np.exp(
            (drift - 0.5 * volatility**2) * dt
            + volatility * np.sqrt(dt) * shock
        )

        prices.append(float(next_price))

    return pd.DataFrame(
        {
            "step": range(n_steps + 1),
            "spot": prices,
        }
    )


def simulate_delta_hedged_call(
    spot: float = 100.0,
    strike: float = 100.0,
    risk_free_rate: float = 0.02,
    implied_volatility: float = 0.20,
    realised_volatility: float = 0.20,
    n_steps: int = 252,
    seed: int = 42,
) -> DeltaHedgeResult:
    """
    Simulate delta hedging for a short European call option.

    Setup:
    - Sell one call option at Black-Scholes price.
    - Delta hedge by buying delta shares.
    - Rebalance each step.
    - Track final hedging P&L.

    This is simplified and ignores funding, dividends, bid/ask spread, and slippage.
    """
    if n_steps <= 1:
        raise ValueError("n_steps must be greater than 1")

    path = simulate_gbm_price_path(
        spot=spot,
        drift=risk_free_rate,
        volatility=realised_volatility,
        n_steps=n_steps,
        seed=seed,
    )

    initial_inputs = OptionInputs(
        spot=spot,
        strike=strike,
        time_to_expiry=1.0,
        risk_free_rate=risk_free_rate,
        volatility=implied_volatility,
    )

    option_premium = black_scholes_call_price(initial_inputs)

    cash = option_premium
    shares = 0.0

    records = []

    for i in range(n_steps):
        current_spot = float(path.loc[i, "spot"])
        time_to_expiry = max((n_steps - i) / TRADING_DAYS_PER_YEAR, 1e-8)

        inputs = OptionInputs(
            spot=current_spot,
            strike=strike,
            time_to_expiry=time_to_expiry,
            risk_free_rate=risk_free_rate,
            volatility=implied_volatility,
        )

        option_price = black_scholes_call_price(inputs)
        delta = call_greeks(inputs).delta

        # Short one call, so hedge by buying delta shares.
        target_shares = delta
        trade_shares = target_shares - shares

        cash -= trade_shares * current_spot
        shares = target_shares

        portfolio_value = cash + shares * current_spot - option_price

        records.append(
            {
                "step": i,
                "spot": current_spot,
                "time_to_expiry": time_to_expiry,
                "option_price": option_price,
                "delta": delta,
                "shares": shares,
                "trade_shares": trade_shares,
                "cash": cash,
                "portfolio_value": portfolio_value,
            }
        )

    final_spot = float(path.loc[n_steps, "spot"])
    payoff = max(final_spot - strike, 0.0)

    # Close hedge and settle option payoff.
    cash += shares * final_spot
    cash -= payoff

    final_pnl = cash

    result = pd.DataFrame(records)
    result["abs_trade_shares"] = result["trade_shares"].abs()

    max_abs_hedge = float(result["shares"].abs().max())
    hedge_turnover = float(result["abs_trade_shares"].sum())

    return DeltaHedgeResult(
        path=result,
        final_pnl=float(final_pnl),
        max_abs_hedge=max_abs_hedge,
        hedge_turnover=hedge_turnover,
    )


if __name__ == "__main__":
    matched_vol = simulate_delta_hedged_call(
        implied_volatility=0.20,
        realised_volatility=0.20,
    )

    high_realised_vol = simulate_delta_hedged_call(
        implied_volatility=0.20,
        realised_volatility=0.35,
    )

    print("Matched implied/realised volatility")
    print(f"Final PnL: {matched_vol.final_pnl:.4f}")
    print(f"Hedge turnover: {matched_vol.hedge_turnover:.4f}")

    print("\nHigh realised volatility")
    print(f"Final PnL: {high_realised_vol.final_pnl:.4f}")
    print(f"Hedge turnover: {high_realised_vol.hedge_turnover:.4f}")
