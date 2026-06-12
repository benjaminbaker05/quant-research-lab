import pandas as pd
import pytest

from src.simulations.coin_market_making import simulate_coin_market_making
from src.simulations.kelly_betting import calculate_kelly_fraction
from src.simulations.markov_chain import simulate_markov_chain
from src.simulations.poisson_arrivals import simulate_poisson_arrivals


def test_coin_market_making_outputs_expected_length():
    result = simulate_coin_market_making(n_trades=100, seed=1)

    assert len(result.trades) == 100
    assert "pnl" in result.trades.columns
    assert "inventory" in result.trades.columns


def test_toxic_flow_reduces_market_maker_pnl():
    clean = simulate_coin_market_making(
        n_trades=10_000,
        informed_flow_prob=0.0,
        seed=1,
    )

    toxic = simulate_coin_market_making(
        n_trades=10_000,
        informed_flow_prob=0.5,
        seed=1,
    )

    assert toxic.total_pnl < clean.total_pnl


def test_poisson_arrivals_positive_event_count():
    result = simulate_poisson_arrivals(
        rate_per_second=1.0,
        horizon_seconds=100.0,
        seed=1,
    )

    assert result.n_events > 0
    assert result.mean_interarrival_time > 0
    assert result.arrival_rate_estimate > 0


def test_markov_chain_state_counts_sum_to_one():
    matrix = pd.DataFrame(
        {
            "down": [0.60, 0.25, 0.15],
            "flat": [0.30, 0.50, 0.30],
            "up": [0.10, 0.25, 0.55],
        },
        index=["down", "flat", "up"],
    )

    result = simulate_markov_chain(
        transition_matrix=matrix,
        initial_state="flat",
        n_steps=1_000,
        seed=1,
    )

    assert result.state_counts.sum() == pytest.approx(1.0)


def test_kelly_fraction_for_positive_edge():
    fraction = calculate_kelly_fraction(
        win_probability=0.55,
        win_loss_ratio=1.0,
    )

    assert fraction == pytest.approx(0.10)