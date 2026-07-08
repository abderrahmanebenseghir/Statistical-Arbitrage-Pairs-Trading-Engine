"""
===========================================================
STATISTICAL ARBITRAGE PAIRS TRADING ENGINE
MAIN PROGRAM
===========================================================
"""

import warnings

warnings.filterwarnings("ignore")

from data import download_data

from cointegration import (
    find_cointegrated_pairs,
    select_best_pair,
)

from strategy import (
    calculate_dynamic_spread,
    calculate_zscore,
    generate_signals,
)

from backtest import backtest_strategy

from performance import (
    performance_metrics,
    create_trade_log,
)

from plots import plot_results

from optimization import optimize_parameters


def main():

    print("=" * 60)
    print("STATISTICAL ARBITRAGE ENGINE")
    print("=" * 60)

    # -----------------------------------
    # Download Data
    # -----------------------------------

    prices = download_data()

    print("\nFirst Five Rows:\n")
    print(prices.head())

    # -----------------------------------
    # Cointegration
    # -----------------------------------

    results = find_cointegrated_pairs(prices)

    asset_a, asset_b = select_best_pair(results)

    # -----------------------------------
    # Strategy
    # -----------------------------------

    spread, hedge_ratios = calculate_dynamic_spread(
        prices,
        asset_a,
        asset_b,
    )

    zscore = calculate_zscore(spread)

    signals = generate_signals(zscore)

    # -----------------------------------
    # Backtest
    # -----------------------------------

    portfolio = backtest_strategy(
        prices,
        asset_a,
        asset_b,
        hedge_ratios,
        signals,
    )

    # -----------------------------------
    # Performance
    # -----------------------------------

    performance_metrics(portfolio)

    # -----------------------------------
    # Parameter Optimization
    # -----------------------------------

    optimization_results = optimize_parameters(
        prices,
        asset_a,
        asset_b,
        spread,
        hedge_ratios,
    )

    print("\n==============================")
    print("BEST PARAMETERS")
    print("==============================")

    print(optimization_results.head())

    # -----------------------------------
    # Trade Log
    # -----------------------------------

    trade_log = create_trade_log(
        portfolio,
        signals,
    )

    print("\n==============================")
    print("TRADE LOG")
    print("==============================")

    print(trade_log.head(20))

    trade_log.to_csv(
        "results/Trade_Log.csv",
        index=True,
    )

    print("\nTrade log exported successfully!")

    # -----------------------------------
    # Charts
    # -----------------------------------

    plot_results(
        prices,
        spread,
        zscore,
        portfolio,
        asset_a,
        asset_b,
    )

    print("\n==============================")
    print("PROJECT COMPLETED")
    print("==============================")


if __name__ == "__main__":
    main()