from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.options.black_scholes import (
    OptionInputs,
    black_scholes_call_price,
    black_scholes_put_price,
    call_greeks,
    put_greeks,
)
from src.options.delta_hedging import simulate_delta_hedged_call
from src.options.implied_vol import implied_volatility


REPORTS_DIR = Path("reports")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    columns = list(df.columns)

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []

    for _, row in df.iterrows():
        row_values = [str(row[column]) for column in columns]
        rows.append("| " + " | ".join(row_values) + " |")

    return "\n".join([header, separator, *rows])


def run_pricing_table() -> pd.DataFrame:
    rows = []

    for volatility in [0.10, 0.20, 0.30, 0.50]:
        inputs = OptionInputs(
            spot=100.0,
            strike=100.0,
            time_to_expiry=1.0,
            risk_free_rate=0.02,
            volatility=volatility,
        )

        call_price = black_scholes_call_price(inputs)
        put_price = black_scholes_put_price(inputs)
        greeks = call_greeks(inputs)

        rows.append(
            {
                "volatility": round(volatility, 4),
                "call_price": round(call_price, 4),
                "put_price": round(put_price, 4),
                "call_delta": round(greeks.delta, 4),
                "call_gamma": round(greeks.gamma, 6),
                "call_vega": round(greeks.vega, 4),
                "call_theta": round(greeks.theta, 4),
            }
        )

    return pd.DataFrame(rows)


def run_implied_vol_example() -> pd.DataFrame:
    inputs = OptionInputs(
        spot=100.0,
        strike=100.0,
        time_to_expiry=1.0,
        risk_free_rate=0.02,
        volatility=0.20,
    )

    call_price = black_scholes_call_price(inputs)

    estimated_iv = implied_volatility(
        market_price=call_price,
        inputs=inputs,
        option_type="call",
    )

    return pd.DataFrame(
        [
            {
                "true_volatility": 0.20,
                "call_price": round(call_price, 4),
                "estimated_implied_volatility": round(estimated_iv, 4),
            }
        ]
    )


def run_delta_hedging_experiments() -> pd.DataFrame:
    rows = []

    scenarios = [
        {
            "scenario": "realised_vol_below_implied",
            "implied_volatility": 0.25,
            "realised_volatility": 0.15,
        },
        {
            "scenario": "realised_vol_equal_implied",
            "implied_volatility": 0.25,
            "realised_volatility": 0.25,
        },
        {
            "scenario": "realised_vol_above_implied",
            "implied_volatility": 0.25,
            "realised_volatility": 0.40,
        },
    ]

    for scenario in scenarios:
        result = simulate_delta_hedged_call(
            implied_volatility=scenario["implied_volatility"],
            realised_volatility=scenario["realised_volatility"],
            seed=42,
        )

        rows.append(
            {
                "scenario": scenario["scenario"],
                "implied_volatility": scenario["implied_volatility"],
                "realised_volatility": scenario["realised_volatility"],
                "final_pnl": round(result.final_pnl, 4),
                "max_abs_hedge": round(result.max_abs_hedge, 4),
                "hedge_turnover": round(result.hedge_turnover, 4),
            }
        )

    return pd.DataFrame(rows)


def save_delta_hedging_plot(output_path: Path) -> None:
    scenarios = {
        "low realised vol": 0.15,
        "matched realised vol": 0.25,
        "high realised vol": 0.40,
    }

    plt.figure(figsize=(10, 6))

    for label, realised_vol in scenarios.items():
        result = simulate_delta_hedged_call(
            implied_volatility=0.25,
            realised_volatility=realised_vol,
            seed=42,
        )

        plt.plot(
            result.path["step"],
            result.path["portfolio_value"],
            label=label,
        )

    plt.title("Delta-Hedged Short Call Portfolio Value")
    plt.xlabel("Step")
    plt.ylabel("Portfolio value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def write_report(
    pricing_table: pd.DataFrame,
    implied_vol_table: pd.DataFrame,
    hedging_table: pd.DataFrame,
    plot_path: Path,
    output_path: Path,
) -> None:
    pricing_markdown = dataframe_to_markdown(pricing_table)
    implied_vol_markdown = dataframe_to_markdown(implied_vol_table)
    hedging_markdown = dataframe_to_markdown(hedging_table)

    report = f"""# Week 7 Report: Options, Greeks, Implied Volatility, and Delta Hedging

## Objective

The objective of this week was to add a mathematical finance module to the project.

This module implements:

- Black-Scholes European call and put pricing
- option Greeks
- implied volatility estimation
- delta hedging simulation

## Why This Matters

Options are central to many market-making and quantitative trading roles. This module demonstrates mathematical modelling, numerical methods, and risk intuition.

## Black-Scholes Pricing

The Black-Scholes model prices European options under simplifying assumptions including:

- lognormal underlying price dynamics
- constant volatility
- constant risk-free rate
- continuous trading
- no transaction costs
- no dividends in this implementation

## Greeks

The implemented Greeks are:

- delta: sensitivity to underlying price
- gamma: sensitivity of delta to underlying price
- vega: sensitivity to volatility
- theta: sensitivity to time decay
- rho: sensitivity to interest rates

## Pricing and Greeks Table

{pricing_markdown}

## Implied Volatility

Implied volatility is the volatility input that makes the model price match the observed market price.

The implementation uses binary search.

{implied_vol_markdown}

## Delta Hedging

The delta hedging simulation sells one call option and dynamically hedges using the underlying asset.

The experiment compares scenarios where realised volatility is below, equal to, or above implied volatility.

{hedging_markdown}

## Delta Hedging Plot

See:

`{plot_path}`

## Interpretation

This module is not intended to be a production options system. It is a mathematical and engineering demonstration.

The key insight is that option risk is multidimensional. A trader is not only exposed to price direction, but also to volatility, time decay, convexity, and hedging error.

The delta hedging experiment shows that hedged option P&L depends on the relationship between implied volatility and realised volatility.

## Limitations

- European options only
- no dividends
- no stochastic volatility
- no volatility smile or surface
- no transaction costs in hedging
- no discrete bid/ask spread
- no funding costs beyond a simple risk-free rate
- simplified daily rebalancing
- no calibration to real options data

## Next Steps

- Add transaction costs to hedging.
- Add discrete hedging frequency comparisons.
- Add volatility surface examples.
- Compare Black-Scholes implied volatility across strikes.
- Connect options module to backtesting/risk framework.
"""

    output_path.write_text(report, encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    pricing_table = run_pricing_table()
    implied_vol_table = run_implied_vol_example()
    hedging_table = run_delta_hedging_experiments()

    plot_path = REPORTS_DIR / "week_7_delta_hedging.png"
    report_path = REPORTS_DIR / "week_7_options_results.md"

    save_delta_hedging_plot(plot_path)

    write_report(
        pricing_table=pricing_table,
        implied_vol_table=implied_vol_table,
        hedging_table=hedging_table,
        plot_path=plot_path,
        output_path=report_path,
    )

    print("\nPricing table:")
    print(pricing_table.to_string(index=False))

    print("\nImplied volatility example:")
    print(implied_vol_table.to_string(index=False))

    print("\nDelta hedging scenarios:")
    print(hedging_table.to_string(index=False))

    print(f"\nSaved plot to {plot_path}")
    print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()