"""
===========================================================
BACKTEST MODULE
===========================================================
"""

import numpy as np
import pandas as pd

from config import Config


# ==========================================================
# BACKTEST ENGINE
# ==========================================================

def backtest_strategy(
    prices,
    asset_a,
    asset_b,
    hedge_ratios,
    signals,
):

    # ------------------------------------------------------
    # Daily Returns
    # ------------------------------------------------------

    returns_a = prices[asset_a].pct_change().fillna(0)

    returns_b = prices[asset_b].pct_change().fillna(0)

    # ------------------------------------------------------
    # Normalize Gross Exposure
    # ------------------------------------------------------

    gross_exposure = (
        1 + hedge_ratios.abs()
    ).replace(0, 1)

    # ------------------------------------------------------
    # Strategy Returns
    # ------------------------------------------------------

    strategy_returns = (
        signals["Position"].shift(1).fillna(0)
        * (
            returns_a
            - hedge_ratios.shift(1).fillna(0) * returns_b
        )
    )

    strategy_returns = (
        strategy_returns
        / gross_exposure.shift(1).fillna(1)
    )

    # ------------------------------------------------------
    # Remove Invalid Values
    # ------------------------------------------------------

    strategy_returns = (
        strategy_returns
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

    # ------------------------------------------------------
    # Prevent Impossible Returns
    # ------------------------------------------------------

    strategy_returns = strategy_returns.clip(
        lower=-0.99,
        upper=0.99,
    )

    # ------------------------------------------------------
    # Trade Detection
    # ------------------------------------------------------

    trades = (
        signals["Position"]
        .diff()
        .abs()
        .fillna(0)
    )

    # ------------------------------------------------------
    # Transaction Costs
    # ------------------------------------------------------

    strategy_returns -= (
        trades * Config.TRANSACTION_COST
    )

    # ------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------

    portfolio = pd.DataFrame(index=prices.index)

    portfolio["Position"] = signals["Position"]

    portfolio["Strategy Return"] = strategy_returns

    portfolio["Equity"] = (
        Config.INITIAL_CAPITAL
        * (1 + strategy_returns).cumprod()
    )

    portfolio["Daily PnL"] = (
        portfolio["Equity"].diff().fillna(0)
    )

    portfolio["Trades"] = trades

    portfolio["Cumulative Return"] = (
        portfolio["Equity"] / Config.INITIAL_CAPITAL - 1
    )

    return portfolio