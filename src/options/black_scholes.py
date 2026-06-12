from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, log, pi, sqrt


@dataclass
class OptionInputs:
    spot: float
    strike: float
    time_to_expiry: float
    risk_free_rate: float
    volatility: float


@dataclass
class Greeks:
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float


def normal_cdf(x: float) -> float:
    """
    Standard normal cumulative distribution function.
    """
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def normal_pdf(x: float) -> float:
    """
    Standard normal probability density function.
    """
    return exp(-0.5 * x * x) / sqrt(2.0 * pi)


def validate_inputs(inputs: OptionInputs) -> None:
    if inputs.spot <= 0:
        raise ValueError("spot must be positive")

    if inputs.strike <= 0:
        raise ValueError("strike must be positive")

    if inputs.time_to_expiry <= 0:
        raise ValueError("time_to_expiry must be positive")

    if inputs.volatility <= 0:
        raise ValueError("volatility must be positive")


def calculate_d1(inputs: OptionInputs) -> float:
    validate_inputs(inputs)

    numerator = log(inputs.spot / inputs.strike) + (
        inputs.risk_free_rate + 0.5 * inputs.volatility**2
    ) * inputs.time_to_expiry

    denominator = inputs.volatility * sqrt(inputs.time_to_expiry)

    return numerator / denominator


def calculate_d2(inputs: OptionInputs) -> float:
    d1 = calculate_d1(inputs)

    return d1 - inputs.volatility * sqrt(inputs.time_to_expiry)


def black_scholes_call_price(inputs: OptionInputs) -> float:
    """
    Price a European call option using the Black-Scholes formula.
    """
    d1 = calculate_d1(inputs)
    d2 = calculate_d2(inputs)

    price = (
        inputs.spot * normal_cdf(d1)
        - inputs.strike
        * exp(-inputs.risk_free_rate * inputs.time_to_expiry)
        * normal_cdf(d2)
    )

    return float(price)


def black_scholes_put_price(inputs: OptionInputs) -> float:
    """
    Price a European put option using the Black-Scholes formula.
    """
    d1 = calculate_d1(inputs)
    d2 = calculate_d2(inputs)

    price = (
        inputs.strike
        * exp(-inputs.risk_free_rate * inputs.time_to_expiry)
        * normal_cdf(-d2)
        - inputs.spot * normal_cdf(-d1)
    )

    return float(price)


def call_greeks(inputs: OptionInputs) -> Greeks:
    """
    Calculate Black-Scholes Greeks for a European call option.
    """
    d1 = calculate_d1(inputs)
    d2 = calculate_d2(inputs)

    delta = normal_cdf(d1)
    gamma = normal_pdf(d1) / (
        inputs.spot * inputs.volatility * sqrt(inputs.time_to_expiry)
    )
    vega = inputs.spot * normal_pdf(d1) * sqrt(inputs.time_to_expiry) / 100.0

    theta = (
        -inputs.spot
        * normal_pdf(d1)
        * inputs.volatility
        / (2.0 * sqrt(inputs.time_to_expiry))
        - inputs.risk_free_rate
        * inputs.strike
        * exp(-inputs.risk_free_rate * inputs.time_to_expiry)
        * normal_cdf(d2)
    ) / 365.0

    rho = (
        inputs.strike
        * inputs.time_to_expiry
        * exp(-inputs.risk_free_rate * inputs.time_to_expiry)
        * normal_cdf(d2)
    ) / 100.0

    return Greeks(
        delta=float(delta),
        gamma=float(gamma),
        vega=float(vega),
        theta=float(theta),
        rho=float(rho),
    )


def put_greeks(inputs: OptionInputs) -> Greeks:
    """
    Calculate Black-Scholes Greeks for a European put option.
    """
    d1 = calculate_d1(inputs)
    d2 = calculate_d2(inputs)

    delta = normal_cdf(d1) - 1.0
    gamma = normal_pdf(d1) / (
        inputs.spot * inputs.volatility * sqrt(inputs.time_to_expiry)
    )
    vega = inputs.spot * normal_pdf(d1) * sqrt(inputs.time_to_expiry) / 100.0

    theta = (
        -inputs.spot
        * normal_pdf(d1)
        * inputs.volatility
        / (2.0 * sqrt(inputs.time_to_expiry))
        + inputs.risk_free_rate
        * inputs.strike
        * exp(-inputs.risk_free_rate * inputs.time_to_expiry)
        * normal_cdf(-d2)
    ) / 365.0

    rho = (
        -inputs.strike
        * inputs.time_to_expiry
        * exp(-inputs.risk_free_rate * inputs.time_to_expiry)
        * normal_cdf(-d2)
    ) / 100.0

    return Greeks(
        delta=float(delta),
        gamma=float(gamma),
        vega=float(vega),
        theta=float(theta),
        rho=float(rho),
    )


if __name__ == "__main__":
    inputs = OptionInputs(
        spot=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    call_price = black_scholes_call_price(inputs)
    put_price = black_scholes_put_price(inputs)
    greeks = call_greeks(inputs)

    print(f"Call price: {call_price:.4f}")
    print(f"Put price: {put_price:.4f}")
    print(greeks)