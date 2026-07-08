"""
===========================================================
PARAMETER OPTIMIZATION MODULE
===========================================================
"""

import numpy as np
import pandas as pd

from strategy import (
    calculate_zscore,
    generate_signals,
)

from backtest import backtest_strategy


# ==========================================================
# GRID SEARCH OPTIMIZATION
# ==========================================================

def optimize_parameters(
    prices,
    asset_a,
    asset_b,
    spread,
    hedge_ratios,
):

    print("\n========================================")
    print("PARAMETER OPTIMIZATION")
    print("========================================")

    entry_values = [1.5, 2.0, 2.5, 3.0]

    exit_values = [0.25, 0.50, 0.75, 1.00]

    optimization_results = []

    zscore = calculate_zscore(spread)

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
                equity.iloc[-1] / equity.iloc[0]
            ) - 1

            volatility = (
                returns.std()
                * np.sqrt(252)
            )

            if returns.std() != 0:

                sharpe = (
                    returns.mean()
                    / returns.std()
                ) * np.sqrt(252)

            else:

                sharpe = 0

            running_max = equity.cummax()

            drawdown = (
                equity - running_max
            ) / running_max

            max_drawdown = drawdown.min()

            optimization_results.append(
                {
                    "Entry": entry,
                    "Exit": exit,
                    "Total Return": total_return,
                    "Sharpe": sharpe,
                    "Max Drawdown": max_drawdown,
                }
            )

    optimization_results = pd.DataFrame(
        optimization_results
    )

    optimization_results = (
        optimization_results
        .sort_values(
            "Sharpe",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    print("\n==============================")
    print("TOP PARAMETER COMBINATIONS")
    print("==============================")

    print(optimization_results.head(10))

    optimization_results.to_csv(
        "results/Optimization.csv",
        index=False,
    )

    return optimization_results