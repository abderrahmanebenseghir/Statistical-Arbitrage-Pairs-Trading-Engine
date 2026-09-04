import numpy as np
import pandas as pd

from backtest import backtest_strategy
from strategy import generate_signals


def calculate_sharpe(returns):
    """Annualized Sharpe ratio based on daily returns."""

    volatility = returns.std()

    if volatility == 0:
        return 0

    return (
        returns.mean() / volatility
    ) * np.sqrt(252)


def optimize_parameters(
    prices,
    asset_a,
    asset_b,
    hedge_ratios,
    zscore,
):
    """
    Test several entry and exit thresholds.

    This is a simple in-sample grid search. It should not be treated
    as out-of-sample validation.
    """

    entry_values = [1.5, 2.0, 2.5, 3.0]
    exit_values = [0.25, 0.50, 0.75, 1.00]

    results = []

    for entry in entry_values:

        for exit in exit_values:

            signals = generate_signals(
                zscore,
                entry=entry,
                exit=exit,
            )

            portfolio = backtest_strategy(
                prices,
                asset_a,
                asset_b,
                hedge_ratios,
                signals,
            )

            returns = portfolio["Strategy Return"]
            equity = portfolio["Equity"]

            total_return = (
                equity.iloc[-1]
                / equity.iloc[0]
            ) - 1

            sharpe = calculate_sharpe(returns)

            running_high = equity.cummax()

            drawdown = (
                equity / running_high
            ) - 1

            max_drawdown = drawdown.min()

            results.append(
                {
                    "Entry Z": entry,
                    "Exit Z": exit,
                    "Total Return": total_return,
                    "Sharpe": sharpe,
                    "Max Drawdown": max_drawdown,
                }
            )

    results = pd.DataFrame(results)

    return results.sort_values(
        "Sharpe",
        ascending=False,
    ).reset_index(drop=True)