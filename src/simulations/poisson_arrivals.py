from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class PoissonArrivalResult:
    arrivals: pd.DataFrame
    n_events: int
    mean_interarrival_time: float
    arrival_rate_estimate: float


def simulate_poisson_arrivals(
    rate_per_second: float = 2.0,
    horizon_seconds: float = 3_600.0,
    seed: int = 42,
) -> PoissonArrivalResult:
    """
    Simulate order arrivals using a Poisson process.

    If arrivals follow a Poisson process, interarrival times are exponentially distributed.
    """
    if rate_per_second <= 0:
        raise ValueError("rate_per_second must be positive")

    if horizon_seconds <= 0:
        raise ValueError("horizon_seconds must be positive")

    rng = np.random.default_rng(seed)

    arrival_times = []
    current_time = 0.0

    while current_time < horizon_seconds:
        interarrival = rng.exponential(1 / rate_per_second)
        current_time += interarrival

        if current_time < horizon_seconds:
            arrival_times.append(current_time)

    arrivals = pd.DataFrame(
        {
            "arrival_time": arrival_times,
        }
    )

    arrivals["interarrival_time"] = arrivals["arrival_time"].diff()
    arrivals.loc[0, "interarrival_time"] = arrivals.loc[0, "arrival_time"]

    n_events = len(arrivals)
    mean_interarrival_time = float(arrivals["interarrival_time"].mean())
    arrival_rate_estimate = n_events / horizon_seconds

    return PoissonArrivalResult(
        arrivals=arrivals,
        n_events=n_events,
        mean_interarrival_time=mean_interarrival_time,
        arrival_rate_estimate=arrival_rate_estimate,
    )


if __name__ == "__main__":
    result = simulate_poisson_arrivals(
        rate_per_second=2.0,
        horizon_seconds=3_600,
    )

    print(f"Number of events: {result.n_events}")
    print(f"Mean interarrival time: {result.mean_interarrival_time:.4f}")
    print(f"Estimated arrival rate: {result.arrival_rate_estimate:.4f} events/sec")