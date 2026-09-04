import numpy as np
import pandas as pd

from config import Config


def backtest_strategy(
    prices,
    asset_a,
    asset_b,
    hedge_ratios,
    signals,
):
    """
    Backtest the pairs strategy using daily close-to-close returns.

    Signals are shifted by one day so that today's signal does not
    receive today's return.
    """

    returns_a = prices[asset_a].pct_change()
    returns_b = prices[asset_b].pct_change()

    hedge = hedge_ratios.shift(1)
    position = signals["Position"].shift(1)

    pair_return = returns_a - hedge * returns_b

    exposure = 1 + hedge.abs()
    exposure = exposure.replace(0, np.nan)

    strategy_returns = (
        position * pair_return / exposure
    )

    strategy_returns = strategy_returns.replace(
        [np.inf, -np.inf],
        np.nan,
    ).fillna(0)

    position_changes = (
        signals["Position"]
        .diff()
        .abs()
        .fillna(0)
    )

    trading_costs = (
        position_changes * Config.TRANSACTION_COST
    )

    strategy_returns = strategy_returns - trading_costs

    equity = (
        Config.INITIAL_CAPITAL
        * (1 + strategy_returns).cumprod()
    )

    portfolio = pd.DataFrame(index=prices.index)

    portfolio["Position"] = signals["Position"]
    portfolio["Strategy Return"] = strategy_returns
    portfolio["Trading Cost"] = trading_costs
    portfolio["Equity"] = equity

    portfolio["Daily PnL"] = equity.diff().fillna(0)

    portfolio["Position Change"] = position_changes

    portfolio["Cumulative Return"] = (
        equity / Config.INITIAL_CAPITAL
    ) - 1

    return portfolio