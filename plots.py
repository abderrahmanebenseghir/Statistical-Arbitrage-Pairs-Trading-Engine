import matplotlib.pyplot as plt


def plot_results(
    prices,
    spread,
    zscore,
    portfolio,
    asset_a,
    asset_b,
):
    """Create the main charts for the strategy."""

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(14, 12),
        sharex=True,
    )

    axes[0].plot(
        prices.index,
        prices[asset_a],
        label=asset_a,
    )

    axes[0].plot(
        prices.index,
        prices[asset_b],
        label=asset_b,
    )

    axes[0].set_title("Asset Prices")
    axes[0].legend()

    axes[1].plot(
        spread.index,
        spread,
        label="Spread",
    )

    axes[1].set_title("Trading Spread")
    axes[1].legend()

    axes[2].plot(
        zscore.index,
        zscore,
        label="Z-Score",
    )

    axes[2].axhline(2, linestyle="--")
    axes[2].axhline(-2, linestyle="--")
    axes[2].axhline(0)

    axes[2].set_title("Spread Z-Score")
    axes[2].legend()

    axes[3].plot(
        portfolio.index,
        portfolio["Equity"],
        label="Portfolio",
    )

    axes[3].set_title("Portfolio Equity")
    axes[3].legend()

    plt.tight_layout()

    plt.savefig(
        "charts/Portfolio_Report.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()