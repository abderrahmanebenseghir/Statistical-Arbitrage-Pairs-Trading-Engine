"""
===========================================================
DATA MODULE
===========================================================
"""

import pandas as pd
import yfinance as yf

from config import Config


def download_data():

    print("=" * 60)
    print("DOWNLOADING MARKET DATA")
    print("=" * 60)

    data = yf.download(
        Config.TICKERS,
        start=Config.START_DATE,
        end=Config.END_DATE,
        auto_adjust=True,
        progress=True,
    )

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data

    prices = prices.ffill().bfill()

    print("Download Complete.")
    print(f"Rows    : {prices.shape[0]}")
    print(f"Assets  : {prices.shape[1]}")

    return prices