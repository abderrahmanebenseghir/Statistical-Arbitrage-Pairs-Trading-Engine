"""
===========================================================
CONFIGURATION
===========================================================
"""

class Config:

    # -------------------------
    # Assets
    # -------------------------
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

    # -------------------------
    # Historical Period
    # -------------------------
    START_DATE = "2018-01-01"
    END_DATE = "2025-01-01"

    # -------------------------
    # Strategy Parameters
    # -------------------------
    INITIAL_CAPITAL = 100000

    ROLLING_WINDOW = 60

    ENTRY_Z = 2.0
    EXIT_Z = 0.5

    TRANSACTION_COST = 0.001