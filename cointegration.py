"""
===========================================================
COINTEGRATION MODULE
===========================================================
"""

from itertools import combinations

import pandas as pd
from statsmodels.tsa.stattools import coint


# ==========================================================
# FIND COINTEGRATED PAIRS
# ==========================================================

def find_cointegrated_pairs(prices):

    print("\nSearching for cointegrated pairs...\n")

    assets = prices.columns

    results = []

    for asset_a, asset_b in combinations(assets, 2):

        try:

            score, pvalue, _ = coint(
                prices[asset_a],
                prices[asset_b],
            )

            corr = prices[asset_a].corr(
                prices[asset_b]
            )

            results.append(
                {
                    "Asset A": asset_a,
                    "Asset B": asset_b,
                    "Correlation": corr,
                    "P-Value": pvalue,
                    "Test Statistic": score,
                }
            )

        except Exception:
            continue

    results = pd.DataFrame(results)

    # ------------------------------------------------------
    # Keep only highly correlated pairs
    # ------------------------------------------------------

    if not results.empty:

        results = results[
            results["Correlation"].abs() >= 0.70
        ]

        results = (
            results
            .sort_values("P-Value")
            .reset_index(drop=True)
        )

    return results


# ==========================================================
# SELECT BEST PAIR
# ==========================================================

def select_best_pair(results):

    if results.empty:

        raise ValueError(
            "No suitable cointegrated pair was found. "
            "Try lowering the minimum correlation threshold."
        )

    best = results.iloc[0]

    asset_a = best["Asset A"]
    asset_b = best["Asset B"]

    print("\n==============================")
    print("BEST PAIR FOUND")
    print("==============================")
    print(f"Asset A      : {asset_a}")
    print(f"Asset B      : {asset_b}")
    print(f"P-Value      : {best['P-Value']:.6f}")
    print(f"Correlation  : {best['Correlation']:.4f}")

    return asset_a, asset_b