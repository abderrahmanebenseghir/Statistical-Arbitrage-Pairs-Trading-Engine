from pathlib import Path

from backtest import backtest_strategy
from cointegration import (
    find_cointegrated_pairs,
    select_best_pair,
)
from data import download_data
from optimization import optimize_parameters
from performance import (
    create_trade_log,
    performance_metrics,
    print_performance,
)
from plots import plot_results
from strategy import (
    calculate_dynamic_spread,
    calculate_zscore,
    generate_signals,
)


def main():

    Path("results").mkdir(exist_ok=True)
    Path("charts").mkdir(exist_ok=True)

    print("\nPairs Trading Research Project")
    print("=" * 40)

    prices = download_data()

    print(
        f"Downloaded {len(prices)} observations "
        f"for {len(prices.columns)} assets."
    )

    print("\nFinding candidate pairs...")

    pair_results = find_cointegrated_pairs(prices)

    if pair_results.empty:
        raise ValueError("No candidate pairs were found.")

    pair_results.to_csv(
        "results/Cointegration.csv",
        index=False,
    )

    asset_a, asset_b = select_best_pair(
        pair_results
    )

    spread, hedge_ratios = calculate_dynamic_spread(
        prices,
        asset_a,
        asset_b,
    )

    zscore = calculate_zscore(spread)

    signals = generate_signals(zscore)

    portfolio = backtest_strategy(
        prices,
        asset_a,
        asset_b,
        hedge_ratios,
        signals,
    )

    results = performance_metrics(portfolio)

    print_performance(results)

    print("\nTesting strategy parameters...")

    optimization = optimize_parameters(
        prices,
        asset_a,
        asset_b,
        hedge_ratios,
        zscore,
    )

    optimization.to_csv(
        "results/Optimization.csv",
        index=False,
    )

    print("\nBest parameter combinations:")
    print(optimization.head())

    trade_log = create_trade_log(
        portfolio
    )

    trade_log.to_csv(
        "results/Trade_Log.csv"
    )

    plot_results(
        prices,
        spread,
        zscore,
        portfolio,
        asset_a,
        asset_b,
    )

    print("\nResults saved to:")
    print("  results/")
    print("  charts/")


if __name__ == "__main__":
    main()