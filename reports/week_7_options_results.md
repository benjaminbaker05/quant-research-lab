# Week 7 Report: Options, Greeks, Implied Volatility, and Delta Hedging

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

| volatility | call_price | put_price | call_delta | call_gamma | call_vega | call_theta |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 5.017 | 3.0368 | 0.5987 | 0.038667 | 0.3867 | -0.0083 |
| 0.2 | 8.916 | 6.9359 | 0.5793 | 0.019552 | 0.391 | -0.0134 |
| 0.3 | 12.8216 | 10.8414 | 0.5858 | 0.01299 | 0.3897 | -0.0185 |
| 0.5 | 20.5512 | 18.5711 | 0.6141 | 0.00765 | 0.3825 | -0.0284 |

## Implied Volatility

Implied volatility is the volatility input that makes the model price match the observed market price.

The implementation uses binary search.

| true_volatility | call_price | estimated_implied_volatility |
| --- | --- | --- |
| 0.2 | 8.916 | 0.2 |

## Delta Hedging

The delta hedging simulation sells one call option and dynamically hedges using the underlying asset.

The experiment compares scenarios where realised volatility is below, equal to, or above implied volatility.

| scenario | implied_volatility | realised_volatility | final_pnl | max_abs_hedge | hedge_turnover |
| --- | --- | --- | --- | --- | --- |
| realised_vol_below_implied | 0.25 | 0.15 | 5.3219 | 0.664 | 4.6005 |
| realised_vol_equal_implied | 0.25 | 0.25 | 1.4941 | 0.7122 | 5.6102 |
| realised_vol_above_implied | 0.25 | 0.4 | -2.4305 | 0.7725 | 5.5964 |

## Delta Hedging Plot

See:

`reports\week_7_delta_hedging.png`

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

## Manual Interpretation Notes

The most important lesson from this module is that options are not simple directional bets.

A call option's value depends on the underlying price, volatility, time to expiry, interest rates, and convexity.

Delta hedging reduces first-order directional exposure, but it does not eliminate risk. The hedger remains exposed to realised volatility, discrete rebalancing error, gamma, transaction costs, and model assumptions.

This module should therefore be interpreted as a mathematical finance demonstration rather than a production-ready options pricing library.
