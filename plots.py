"""
===========================================================
PLOTTING MODULE
===========================================================
"""

import matplotlib.pyplot as plt


def plot_results(
    prices,
    spread,
    zscore,
    portfolio,
    asset_a,
    asset_b
):

    plt.style.use("ggplot")

    fig = plt.figure(figsize=(16, 14))

    # -------------------------
    # Asset Prices
    # -------------------------

    ax1 = plt.subplot(4, 1, 1)

    ax1.plot(
        prices.index,
        prices[asset_a],
        label=asset_a
    )

    ax1.plot(
        prices.index,
        prices[asset_b],
        label=asset_b
    )

    ax1.set_title("Asset Prices")

    ax1.legend()

    # -------------------------
    # Spread
    # -------------------------

    ax2 = plt.subplot(4, 1, 2)

    ax2.plot(
        spread.index,
        spread,
        label="Spread"
    )

    ax2.set_title("Spread")

    ax2.legend()

    # -------------------------
    # Z-Score
    # -------------------------

    ax3 = plt.subplot(4, 1, 3)

    ax3.plot(
        zscore.index,
        zscore,
        label="Z-Score"
    )

    ax3.axhline(
        2,
        linestyle="--"
    )

    ax3.axhline(
        -2,
        linestyle="--"
    )

    ax3.axhline(
        0,
        linestyle="-"
    )

    ax3.set_title("Rolling Z-Score")

    ax3.legend()

    # -------------------------
    # Equity Curve
    # -------------------------

    ax4 = plt.subplot(4, 1, 4)

    ax4.plot(
        portfolio.index,
        portfolio["Equity"],
        label="Portfolio"
    )

    ax4.set_title("Portfolio Equity")

    ax4.legend()

    plt.tight_layout()

    plt.savefig(
        "charts/Portfolio_Report.png",
        dpi=300
    )

    plt.show()