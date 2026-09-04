class Config:
    """Main settings for the pairs trading experiment."""

    TICKERS = [
        "SPY",
        "QQQ",
        "IWM",
        "GLD",
        "SLV",
        "XLE",
        "XOP",
        "XOM",
        "CVX",
        "COP",
        "XLK",
    ]

    START_DATE = "2018-01-01"
    END_DATE = "2025-01-01"

    INITIAL_CAPITAL = 100_000

    ROLLING_WINDOW = 60

    ENTRY_Z = 2.0
    EXIT_Z = 0.5

    MIN_CORRELATION = 0.70
    MAX_COINT_PVALUE = 0.05

    TRANSACTION_COST = 0.001