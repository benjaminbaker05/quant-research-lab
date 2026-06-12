from __future__ import annotations

from dataclasses import replace

from src.options.black_scholes import (
    OptionInputs,
    black_scholes_call_price,
    black_scholes_put_price,
)


def implied_volatility(
    market_price: float,
    inputs: OptionInputs,
    option_type: str = "call",
    low_vol: float = 1e-6,
    high_vol: float = 5.0,
    tolerance: float = 1e-6,
    max_iterations: int = 100,
) -> float:
    """
    Estimate implied volatility using binary search.

    Implied volatility is the volatility input that makes the model price
    match the observed market price.
    """
    if market_price <= 0:
        raise ValueError("market_price must be positive")

    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    if low_vol <= 0 or high_vol <= 0:
        raise ValueError("volatility bounds must be positive")

    if low_vol >= high_vol:
        raise ValueError("low_vol must be below high_vol")

    def price_at_vol(volatility: float) -> float:
        trial_inputs = replace(inputs, volatility=volatility)

        if option_type == "call":
            return black_scholes_call_price(trial_inputs)

        return black_scholes_put_price(trial_inputs)

    low_price = price_at_vol(low_vol)
    high_price = price_at_vol(high_vol)

    if not low_price <= market_price <= high_price:
        raise ValueError(
            "market_price is outside the model price range for the volatility bounds"
        )

    low = low_vol
    high = high_vol

    for _ in range(max_iterations):
        mid = 0.5 * (low + high)
        mid_price = price_at_vol(mid)

        if abs(mid_price - market_price) < tolerance:
            return float(mid)

        if mid_price < market_price:
            low = mid
        else:
            high = mid

    return float(0.5 * (low + high))


if __name__ == "__main__":
    inputs = OptionInputs(
        spot=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    market_price = black_scholes_call_price(inputs)

    estimated_iv = implied_volatility(
        market_price=market_price,
        inputs=inputs,
        option_type="call",
    )

    print(f"Market price: {market_price:.4f}")
    print(f"Estimated implied volatility: {estimated_iv:.4f}")