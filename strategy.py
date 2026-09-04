import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import Config


def calculate_dynamic_spread(prices, asset_a, asset_b):
    """
    Estimate a rolling hedge ratio and use it to construct the spread.

    The regression is:

        asset_a = alpha + beta * asset_b + error

    The residual component is used as the trading spread.
    """

    window = Config.ROLLING_WINDOW

    hedge_ratios = pd.Series(
        index=prices.index,
        dtype=float,
        name="Hedge Ratio",
    )

    spread = pd.Series(
        index=prices.index,
        dtype=float,
        name="Spread",
    )

    for end in range(window, len(prices) + 1):
        start = end - window

        y = prices[asset_a].iloc[start:end]
        x = prices[asset_b].iloc[start:end]

        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()

        beta = model.params.iloc[1]

        current_date = prices.index[end - 1]

        hedge_ratios.loc[current_date] = beta

        spread.loc[current_date] = (
            prices[asset_a].loc[current_date]
            - beta * prices[asset_b].loc[current_date]
        )

    return spread, hedge_ratios


def calculate_zscore(spread):
    """Calculate the rolling z-score of the trading spread."""

    window = Config.ROLLING_WINDOW

    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()

    std = std.replace(0, np.nan)

    return (spread - mean) / std


def generate_signals(
    zscore,
    entry=Config.ENTRY_Z,
    exit=Config.EXIT_Z,
):
    """
    Create positions from the spread z-score.

    +1 = long the spread
    -1 = short the spread
     0 = flat
    """

    position = pd.Series(
        index=zscore.index,
        dtype=float,
        name="Position",
    )

    current_position = 0

    for date, value in zscore.items():

        if pd.isna(value):
            position.loc[date] = 0
            continue

        if current_position == 0:

            if value <= -entry:
                current_position = 1

            elif value >= entry:
                current_position = -1

        elif current_position == 1:

            if value >= -exit:
                current_position = 0

        elif current_position == -1:

            if value <= exit:
                current_position = 0

        position.loc[date] = current_position

    signals = pd.DataFrame(index=zscore.index)

    signals["Z-Score"] = zscore
    signals["Position"] = position

    return signals