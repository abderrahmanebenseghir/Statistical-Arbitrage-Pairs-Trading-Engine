""import pandas as pd
import yfinance as yf

from config import Config


def download_data():
    """Download adjusted historical prices for the selected assets."""

    data = yf.download(
        Config.TICKERS,
        start=Config.START_DATE,
        end=Config.END_DATE,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError("No market data was returned.")

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"].copy()
    else:
        prices = data[["Close"]].copy()
        prices.columns = [Config.TICKERS[0]]

    prices = prices.sort_index()
    prices = prices.ffill()

    # Remove rows where we still do not have enough information.
    prices = prices.dropna(how="all")

    if prices.empty:
        raise ValueError("Price data is empty after cleaning.")

    return prices