from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class MarketMakingResult:
    trades: pd.DataFrame
    total_pnl: float
    mean_pnl: float
    pnl_std: float
    final_inventory: int


def simulate_coin_market_making(
    true_prob_heads: float = 0.55,
    estimated_prob_heads: float = 0.55,
    spread: float = 0.04,
    n_trades: int = 10_000,
    informed_flow_prob: float = 0.0,
    seed: int = 42,
) -> MarketMakingResult:
    """
    Simulate a simple market maker quoting a binary asset.

    The asset pays:
    - 1 if heads
    - 0 if tails

    The market maker estimates fair value as estimated_prob_heads.

    They quote:
    - bid = fair_value - spread / 2
    - ask = fair_value + spread / 2

    Random traders buy or sell with equal probability.
    Informed traders buy if the outcome is heads and sell if the outcome is tails.
    """
    if not 0 <= true_prob_heads <= 1:
        raise ValueError("true_prob_heads must be between 0 and 1")

    if not 0 <= estimated_prob_heads <= 1:
        raise ValueError("estimated_prob_heads must be between 0 and 1")

    if not 0 <= informed_flow_prob <= 1:
        raise ValueError("informed_flow_prob must be between 0 and 1")

    rng = np.random.default_rng(seed)

    fair_value = estimated_prob_heads
    bid = fair_value - spread / 2
    ask = fair_value + spread / 2

    outcomes = rng.binomial(1, true_prob_heads, size=n_trades)
    informed = rng.random(n_trades) < informed_flow_prob

    sides = []

    for i in range(n_trades):
        if informed[i]:
            # Informed trader buys from us when asset pays 1,
            # and sells to us when asset pays 0.
            side = "customer_buys" if outcomes[i] == 1 else "customer_sells"
        else:
            side = "customer_buys" if rng.random() < 0.5 else "customer_sells"

        sides.append(side)

    pnl = []
    inventory = []

    current_inventory = 0

    for outcome, side in zip(outcomes, sides):
        if side == "customer_buys":
            # We sell at ask and later pay the asset outcome.
            trade_pnl = ask - outcome
            current_inventory -= 1
        else:
            # We buy at bid and later receive the asset outcome.
            trade_pnl = outcome - bid
            current_inventory += 1

        pnl.append(trade_pnl)
        inventory.append(current_inventory)

    trades = pd.DataFrame(
        {
            "outcome": outcomes,
            "side": sides,
            "pnl": pnl,
            "cumulative_pnl": np.cumsum(pnl),
            "inventory": inventory,
        }
    )

    return MarketMakingResult(
        trades=trades,
        total_pnl=float(trades["pnl"].sum()),
        mean_pnl=float(trades["pnl"].mean()),
        pnl_std=float(trades["pnl"].std()),
        final_inventory=int(trades["inventory"].iloc[-1]),
    )


if __name__ == "__main__":
    clean_flow = simulate_coin_market_making(informed_flow_prob=0.0)
    toxic_flow = simulate_coin_market_making(informed_flow_prob=0.3)

    print("Clean flow")
    print(f"Total PnL: {clean_flow.total_pnl:.4f}")
    print(f"Mean PnL per trade: {clean_flow.mean_pnl:.6f}")
    print(f"Final inventory: {clean_flow.final_inventory}")

    print("\nToxic flow")
    print(f"Total PnL: {toxic_flow.total_pnl:.4f}")
    print(f"Mean PnL per trade: {toxic_flow.mean_pnl:.6f}")
    print(f"Final inventory: {toxic_flow.final_inventory}")