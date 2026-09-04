import numpy as np
import pandas as pd


def performance_metrics(portfolio):
    """Calculate the main performance statistics."""

    returns = portfolio["Strategy Return"]
    equity = portfolio["Equity"]

    total_return = (
        equity.iloc[-1] / equity.iloc[0]
    ) - 1

    number_of_days = len(equity)

    years = number_of_days / 252

    if years > 0:
        annual_return = (
            (equity.iloc[-1] / equity.iloc[0])
            ** (1 / years)
        ) - 1
    else:
        annual_return = 0

    annual_volatility = returns.std() * np.sqrt(252)

    if returns.std() > 0:
        sharpe = (
            returns.mean()
            / returns.std()
        ) * np.sqrt(252)
    else:
        sharpe = 0

    running_high = equity.cummax()

    drawdown = (
        equity / running_high
    ) - 1

    max_drawdown = drawdown.min()

    if max_drawdown < 0:
        calmar = annual_return / abs(max_drawdown)
    else:
        calmar = np.nan

    gross_profit = returns[returns > 0].sum()

    gross_loss = abs(
        returns[returns < 0].sum()
    )

    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    else:
        profit_factor = np.nan

    trades = int(
        portfolio["Position Change"].sum()
    )

    results = {
        "Total Return": total_return,
        "Annual Return": annual_return,
        "Annual Volatility": annual_volatility,
        "Sharpe Ratio": sharpe,
        "Calmar Ratio": calmar,
        "Profit Factor": profit_factor,
        "Maximum Drawdown": max_drawdown,
        "Position Changes": trades,
    }

    return results


def print_performance(results):
    """Print the performance results in a readable format."""

    print("\nPerformance")
    print("-" * 30)

    for name, value in results.items():

        if "Return" in name or "Volatility" in name:
            print(f"{name}: {value:.2%}")

        elif "Drawdown" in name:
            print(f"{name}: {value:.2%}")

        elif "Ratio" in name or "Factor" in name:
            print(f"{name}: {value:.2f}")

        else:
            print(f"{name}: {value}")


def create_trade_log(portfolio):
    """Return dates where the position changed."""

    changes = portfolio[
        portfolio["Position Change"] > 0
    ].copy()

    if changes.empty:
        return pd.DataFrame(
            columns=["Position", "Action"]
        )

    changes["Action"] = np.where(
        changes["Position"] > 0,
        "LONG",
        "SHORT",
    )

    return changes[
        ["Position", "Action"]
    ]