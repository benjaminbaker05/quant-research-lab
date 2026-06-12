from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class MarkovChainResult:
    states: pd.DataFrame
    state_counts: pd.Series
    transition_matrix: pd.DataFrame


def simulate_markov_chain(
    transition_matrix: pd.DataFrame,
    initial_state: str,
    n_steps: int = 1_000,
    seed: int = 42,
) -> MarkovChainResult:
    """
    Simulate a Markov chain.

    The next state depends only on the current state.
    """
    if initial_state not in transition_matrix.index:
        raise ValueError("initial_state must be in transition matrix index")

    if set(transition_matrix.index) != set(transition_matrix.columns):
        raise ValueError("transition matrix index and columns must match")

    row_sums = transition_matrix.sum(axis=1)

    if not np.allclose(row_sums.values, 1.0):
        raise ValueError("each transition matrix row must sum to 1")

    rng = np.random.default_rng(seed)

    current_state = initial_state
    states = [current_state]

    for _ in range(n_steps - 1):
        probabilities = transition_matrix.loc[current_state].values
        possible_states = transition_matrix.columns.values

        current_state = rng.choice(possible_states, p=probabilities)
        states.append(current_state)

    states_df = pd.DataFrame({"state": states})
    state_counts = states_df["state"].value_counts(normalize=True)

    return MarkovChainResult(
        states=states_df,
        state_counts=state_counts,
        transition_matrix=transition_matrix,
    )


if __name__ == "__main__":
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
        n_steps=10_000,
    )

    print("Long-run state frequencies:")
    print(result.state_counts)