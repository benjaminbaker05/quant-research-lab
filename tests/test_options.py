import pytest

from src.options.black_scholes import (
    OptionInputs,
    black_scholes_call_price,
    black_scholes_put_price,
    call_greeks,
)
from src.options.delta_hedging import (
    simulate_delta_hedged_call,
    simulate_gbm_price_path,
)
from src.options.implied_vol import implied_volatility


def test_black_scholes_call_price_is_positive():
    inputs = OptionInputs(
        spot=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    price = black_scholes_call_price(inputs)

    assert price > 0


def test_put_call_parity_approximately_holds():
    from math import exp

    inputs = OptionInputs(
        spot=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    call = black_scholes_call_price(inputs)
    put = black_scholes_put_price(inputs)

    left_side = call - put
    right_side = inputs.spot - inputs.strike * exp(
        -inputs.risk_free_rate * inputs.time_to_expiry
    )

    assert left_side == pytest.approx(right_side, abs=1e-4)


def test_call_delta_between_zero_and_one():
    inputs = OptionInputs(
        spot=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    greeks = call_greeks(inputs)

    assert 0.0 < greeks.delta < 1.0


def test_implied_volatility_recovers_input_volatility():
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

    assert estimated_iv == pytest.approx(0.20, abs=1e-4)


def test_gbm_price_path_has_expected_length():
    path = simulate_gbm_price_path(
        spot=100.0,
        volatility=0.20,
        n_steps=10,
        seed=1,
    )

    assert len(path) == 11
    assert "spot" in path.columns


def test_delta_hedging_outputs_pnl():
    result = simulate_delta_hedged_call(
        spot=100.0,
        strike=100.0,
        implied_volatility=0.20,
        realised_volatility=0.20,
        n_steps=30,
        seed=1,
    )

    assert "portfolio_value" in result.path.columns
    assert isinstance(result.final_pnl, float)
    assert result.hedge_turnover >= 0