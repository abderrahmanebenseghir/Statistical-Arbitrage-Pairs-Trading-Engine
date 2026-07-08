"""
===========================================================
STRATEGY MODULE
===========================================================
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import Config


# ==========================================================
# DYNAMIC HEDGE RATIO
# ==========================================================

def calculate_dynamic_spread(prices, asset_a, asset_b):

    hedge_ratios = []

    spreads = []

    index = prices.index

    window = Config.ROLLING_WINDOW

    for i in range(len(prices)):

        if i < window:

            hedge_ratios.append(np.nan)
            spreads.append(np.nan)
            continue

        y = prices[asset_a].iloc[i - window:i]

        x = prices[asset_b].iloc[i - window:i]

        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()

        beta = model.params.iloc[1]

        hedge_ratios.append(beta)

        spread = (
            prices[asset_a].iloc[i]
            - beta * prices[asset_b].iloc[i]
        )

        spreads.append(spread)

    hedge_ratios = pd.Series(
        hedge_ratios,
        index=index,
        name="Beta"
    )

    spreads = pd.Series(
        spreads,
        index=index,
        name="Spread"
    )

    print("\nDynamic hedge ratio created.")

    return spreads, hedge_ratios


# ==========================================================
# ROLLING Z-SCORE
# ==========================================================

def calculate_zscore(spread):

    rolling_mean = spread.rolling(
        Config.ROLLING_WINDOW
    ).mean()

    rolling_std = (
        spread
        .rolling(Config.ROLLING_WINDOW)
        .std()
        .replace(0, np.nan)
    )

    zscore = (
        spread - rolling_mean
    ) / rolling_std

    zscore = (
        zscore
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    return zscore


# ==========================================================
# SIGNAL GENERATION
# ==========================================================

def generate_signals(
    zscore,
    entry=Config.ENTRY_Z,
    exit=Config.EXIT_Z,
):

    signals = pd.DataFrame(index=zscore.index)

    signals["Z-Score"] = zscore

    signals["Position"] = 0

    # Long Spread
    signals.loc[
        zscore < -entry,
        "Position"
    ] = 1

    # Short Spread
    signals.loc[
        zscore > entry,
        "Position"
    ] = -1

    # Exit
    signals.loc[
        zscore.abs() < exit,
        "Position"
    ] = 0

    signals["Position"] = (
        signals["Position"]
        .replace(0, np.nan)
        .ffill()
        .fillna(0)
    )

    return signals