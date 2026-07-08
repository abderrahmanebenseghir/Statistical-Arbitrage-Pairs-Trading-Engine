"""
===========================================================
PERFORMANCE MODULE
===========================================================
"""

import numpy as np
import pandas as pd


# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

def performance_metrics(portfolio):

    returns = portfolio["Strategy Return"]

    equity = portfolio["Equity"]

    total_return = (
        equity.iloc[-1] / equity.iloc[0]
    ) - 1

    annual_return = (
        (equity.iloc[-1] / equity.iloc[0])
        ** (252 / len(equity))
        - 1
    )

    annual_volatility = (
        returns.std()
        * np.sqrt(252)
    )

    # --------------------------------------
    # Sharpe Ratio
    # --------------------------------------

    if returns.std() != 0:

        sharpe = (
            returns.mean()
            / returns.std()
        ) * np.sqrt(252)

    else:

        sharpe = 0

    # --------------------------------------
    # Drawdown
    # --------------------------------------

    running_max = equity.cummax()

    drawdown = (
        equity - running_max
    ) / running_max

    max_drawdown = drawdown.min()

    # --------------------------------------
    # Trades
    # --------------------------------------

    total_trades = int(
        portfolio["Trades"].sum()
    )

    # --------------------------------------
    # Win Rate
    # --------------------------------------

    winning_days = (returns > 0).sum()

    losing_days = (returns < 0).sum()

    total_days = winning_days + losing_days

    if total_days > 0:

        win_rate = winning_days / total_days

    else:

        win_rate = 0

    # --------------------------------------
    # Profit Factor
    # --------------------------------------

    gross_profit = returns[
        returns > 0
    ].sum()

    gross_loss = abs(
        returns[
            returns < 0
        ].sum()
    )

    if gross_loss != 0:

        profit_factor = (
            gross_profit / gross_loss
        )

    else:

        profit_factor = np.inf

    # --------------------------------------
    # Calmar Ratio
    # --------------------------------------

    if max_drawdown != 0:

        calmar = (
            annual_return
            / abs(max_drawdown)
        )

    else:

        calmar = np.inf

    print("\n==============================")
    print("PERFORMANCE")
    print("==============================")
    print(f"Total Return     : {total_return:.2%}")
    print(f"Annual Return    : {annual_return:.2%}")
    print(f"Volatility       : {annual_volatility:.2%}")
    print(f"Sharpe Ratio     : {sharpe:.2f}")
    print(f"Calmar Ratio     : {calmar:.2f}")
    print(f"Profit Factor    : {profit_factor:.2f}")
    print(f"Max Drawdown     : {max_drawdown:.2%}")
    print(f"Trades Executed  : {total_trades}")
    print(f"Win Rate         : {win_rate:.2%}")

    return {
        "Total Return": total_return,
        "Annual Return": annual_return,
        "Volatility": annual_volatility,
        "Sharpe": sharpe,
        "Calmar": calmar,
        "Profit Factor": profit_factor,
        "Max Drawdown": max_drawdown,
        "Trades": total_trades,
        "Win Rate": win_rate,
    }


# ==========================================================
# TRADE LOG
# ==========================================================

def create_trade_log(portfolio, signals):

    trades = pd.DataFrame(index=portfolio.index)

    trades["Position"] = signals["Position"]

    trades["Trade"] = (
        trades["Position"]
        .diff()
    )

    trade_log = trades[
        trades["Trade"] != 0
    ].copy()

    trade_log["Action"] = np.where(
        trade_log["Trade"] > 0,
        "BUY",
        "SELL"
    )

    trade_log.drop(
        columns=["Trade"],
        inplace=True
    )

    return trade_log