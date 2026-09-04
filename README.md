# Statistical Arbitrage Pairs Trading

A Python research project exploring a simple statistical arbitrage strategy based on
cointegration and mean reversion.

The project downloads historical market data, searches for potentially cointegrated
asset pairs, estimates a rolling hedge ratio, calculates the spread and its z-score,
generates trading signals, and evaluates the strategy through a historical backtest.

## What I wanted to explore

The main question behind the project was:

> Can two assets that historically move together be traded when their relationship
> temporarily moves away from its usual level?

The strategy treats large deviations in the spread as potential mean-reversion
opportunities.

## Strategy

The research pipeline is:

1. Download historical price data.
2. Test possible asset pairs for cointegration.
3. Select a statistically significant pair.
4. Estimate a rolling hedge ratio using OLS.
5. Construct the spread.
6. Calculate a rolling z-score.
7. Generate long/short signals from the z-score.
8. Backtest the strategy using historical returns.
9. Include transaction costs.
10. Calculate performance statistics.
11. Test different entry and exit thresholds.

## Project Structure

```text
.
├── main.py
├── config.py
├── data.py
├── cointegration.py
├── strategy.py
├── backtest.py
├── performance.py
├── optimization.py
├── plots.py
├── requirements.txt
│
├── results/
└── charts/