from itertools import combinations

import pandas as pd
from statsmodels.tsa.stattools import coint

from config import Config


def find_cointegrated_pairs(prices):
    """
    Test every possible pair using the Engle-Granger test.

    Pairs with a strong enough correlation and a statistically
    significant cointegration test are kept.
    """

    results = []

    for asset_a, asset_b in combinations(prices.columns, 2):
        pair = prices[[asset_a, asset_b]].dropna()

        if len(pair) < Config.ROLLING_WINDOW:
            continue

        correlation = pair[asset_a].corr(pair[asset_b])

        if abs(correlation) < Config.MIN_CORRELATION:
            continue

        try:
            test_stat, p_value, _ = coint(
                pair[asset_a],
                pair[asset_b],
            )
        except Exception:
            continue

        results.append(
            {
                "Asset A": asset_a,
                "Asset B": asset_b,
                "Correlation": correlation,
                "Test Statistic": test_stat,
                "P-Value": p_value,
            }
        )

    if not results:
        return pd.DataFrame(
            columns=[
                "Asset A",
                "Asset B",
                "Correlation",
                "Test Statistic",
                "P-Value",
            ]
        )

    results = pd.DataFrame(results)

    results = results.sort_values("P-Value").reset_index(drop=True)

    return results


def select_best_pair(results):
    """Return the pair with the strongest cointegration result."""

    if results.empty:
        raise ValueError(
            "No suitable pair was found. "
            "Try changing the correlation or p-value thresholds."
        )

    significant = results[
        results["P-Value"] <= Config.MAX_COINT_PVALUE
    ]

    if significant.empty:
        raise ValueError(
            "No pair passed the cointegration significance threshold."
        )

    best = significant.iloc[0]

    asset_a = best["Asset A"]
    asset_b = best["Asset B"]

    print("\nBest pair")
    print("-" * 30)
    print(f"Asset A: {asset_a}")
    print(f"Asset B: {asset_b}")
    print(f"Correlation: {best['Correlation']:.3f}")
    print(f"P-value: {best['P-Value']:.5f}")

    return asset_a, asset_b