# Probability for Trading

## Why probability matters in quant trading

Trading decisions are made under uncertainty. A quant does not ask, "Will this definitely happen?" Instead, they ask:

- What is the probability distribution?
- What is the expected value?
- What is the risk?
- What happens in the tail?
- How does my estimate change with new information?

## Expected Value

Expected value is the probability-weighted average outcome.

For a random variable X:

E[X] = sum of each outcome times its probability.

Example:

A bet pays £10 with probability 0.55 and loses £10 with probability 0.45.

Expected value:

E[X] = 0.55 * 10 + 0.45 * (-10) = 1

So the expected profit is £1 per bet.

## Variance

Expected value is not enough. Two strategies can have the same expected value but very different risk.

Variance measures how spread out outcomes are.

High variance means more uncertainty and larger drawdowns.

## Conditional Probability

Conditional probability asks:

What is the probability of A given that B has happened?

In trading, this matters because new information changes the probabilities.

Example:

- Probability price goes up: P(up)
- Probability price goes up given large buy imbalance: P(up | imbalance)

If P(up | imbalance) > P(up), the imbalance may contain predictive information.

## Bayes' Rule

Bayes' rule updates beliefs after seeing evidence.

P(A | B) = P(B | A)P(A) / P(B)

Trading interpretation:

- A = price will move up
- B = observed signal

Bayes' rule helps us think about whether a signal genuinely changes our belief.

## Market Making

A market maker quotes two prices:

- bid: price they are willing to buy at
- ask: price they are willing to sell at

The spread is:

ask - bid

Market makers try to earn the spread, but face risks:

1. Inventory risk
2. Adverse selection
3. Volatility risk
4. Latency risk

## Inventory Risk

If a market maker buys too much, they become long inventory.

If the price falls, they lose money.

If they sell too much, they become short inventory.

If the price rises, they lose money.

## Adverse Selection

Adverse selection happens when informed traders trade against the market maker.

Example:

If someone knows the true value is about to rise, they buy from the market maker before the quote updates.

The market maker sells too cheaply and loses money.

## Poisson Arrivals

Order arrivals are often modelled as random events over time.

A simple model assumes trades arrive according to a Poisson process.

This is not perfectly realistic, but it is a useful first model.

## Markov Chains

A Markov chain models a system where the next state depends only on the current state.

In trading, simple Markov models can be used to model:

- price direction
- volatility regimes
- order-flow states
- liquidity states

## Kelly Criterion

Kelly sizing gives the fraction of capital to bet when you have an edge.

It maximises long-run logarithmic growth, but full Kelly can be very aggressive.

In practice, traders often use fractional Kelly.