from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class KellySimulationResult:
    wealth_path: pd.DataFrame
    final_wealth: float
    max_drawdown: float
    kelly_fraction: float


def calculate_kelly_fraction(
    win_probability: float,
    win_loss_ratio: float,
) -> float:
    """
    Calculate the Kelly fraction for a binary bet.

    win_loss_ratio is the amount won per 1 unit lost.
    """
    if not 0 <= win_probability <= 1:
        raise ValueError("win_probability must be between 0 and 1")

    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be positive")

    q = 1 - win_probability
    fraction = (win_loss_ratio * win_probability - q) / win_loss_ratio

    return max(0.0, fraction)


def simulate_kelly_betting(
    win_probability: float = 0.55,
    win_loss_ratio: float = 1.0,
    fraction_multiplier: float = 1.0,
    n_bets: int = 1_000,
    initial_wealth: float = 1.0,
    seed: int = 42,
) -> KellySimulationResult:
    """
    Simulate repeated betting using a Kelly fraction.

    fraction_multiplier allows fractional Kelly:
    - 1.0 = full Kelly
    - 0.5 = half Kelly
    - 0.25 = quarter Kelly
    """
    if initial_wealth <= 0:
        raise ValueError("initial_wealth must be positive")

    if n_bets <= 0:
        raise ValueError("n_bets must be positive")

    if fraction_multiplier < 0:
        raise ValueError("fraction_multiplier must be non-negative")

    rng = np.random.default_rng(seed)

    full_kelly = calculate_kelly_fraction(
        win_probability=win_probability,
        win_loss_ratio=win_loss_ratio,
    )

    bet_fraction = full_kelly * fraction_multiplier

    wealth = initial_wealth
    wealth_values = [wealth]

    outcomes = rng.random(n_bets) < win_probability

    for won in outcomes:
        stake = wealth * bet_fraction

        if won:
            wealth += stake * win_loss_ratio
        else:
            wealth -= stake

        wealth_values.append(wealth)

    wealth_path = pd.DataFrame({"wealth": wealth_values})
    wealth_path["running_max"] = wealth_path["wealth"].cummax()
    wealth_path["drawdown"] = (
        wealth_path["wealth"] / wealth_path["running_max"] - 1
    )

    final_wealth = float(wealth_path["wealth"].iloc[-1])
    max_drawdown = float(wealth_path["drawdown"].min())

    return KellySimulationResult(
        wealth_path=wealth_path,
        final_wealth=final_wealth,
        max_drawdown=max_drawdown,
        kelly_fraction=bet_fraction,
    )


if __name__ == "__main__":
    full_kelly = simulate_kelly_betting(fraction_multiplier=1.0)
    half_kelly = simulate_kelly_betting(fraction_multiplier=0.5)

    print("Full Kelly")
    print(f"Kelly fraction: {full_kelly.kelly_fraction:.4f}")
    print(f"Final wealth: {full_kelly.final_wealth:.4f}")
    print(f"Max drawdown: {full_kelly.max_drawdown:.2%}")

    print("\nHalf Kelly")
    print(f"Kelly fraction: {half_kelly.kelly_fraction:.4f}")
    print(f"Final wealth: {half_kelly.final_wealth:.4f}")
    print(f"Max drawdown: {half_kelly.max_drawdown:.2%}")