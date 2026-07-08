# Statistical Arbitrage Pairs Trading Engine

A professional quantitative trading engine written in Python that implements a **Statistical Arbitrage (Pairs Trading)** strategy using **cointegration** and **mean reversion**.

The engine automatically identifies cointegrated asset pairs, estimates dynamic hedge ratios using rolling Ordinary Least Squares (OLS), generates trading signals through rolling Z-Scores, backtests the strategy with transaction costs, evaluates performance using professional risk metrics, and exports reports and visualizations.

This project was developed as a quantitative finance portfolio project and serves as the foundation for the future **QuantLab** quantitative research framework.

---

# Features

- Live market data from Yahoo Finance
- Automatic pair discovery
- Engle-Granger cointegration testing
- Dynamic rolling hedge ratio (OLS)
- Rolling Z-Score calculation
- Mean reversion trading strategy
- Transaction cost modeling
- Professional backtesting engine
- Portfolio equity tracking
- Performance analytics
- Parameter optimization (Grid Search)
- Trade log export (CSV)
- Optimization report (CSV)
- Professional visualizations
- Modular Python architecture

---

# Methodology

The strategy follows the workflow below:

1. Download historical market data.
2. Identify cointegrated asset pairs using the Engle-Granger test.
3. Estimate a rolling hedge ratio using Ordinary Least Squares (OLS).
4. Construct the spread between the two assets.
5. Compute the rolling Z-Score.
6. Generate entry and exit signals.
7. Backtest the strategy with transaction costs.
8. Evaluate performance using professional risk-adjusted metrics.
9. Optimize strategy parameters using Grid Search.

---

# Project Structure

```
QuantFinanceProjects/

│
├── main.py
├── config.py
├── data.py
├── cointegration.py
├── strategy.py
├── backtest.py
├── performance.py
├── optimization.py
├── plots.py
│
├── results/
│   ├── Trade_Log.csv
│   └── Optimization.csv
│
└── charts/
```

---

# Technologies

- Python
- Pandas
- NumPy
- Statsmodels
- SciPy
- Matplotlib
- Seaborn
- yfinance

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Run

```bash
python main.py
```

---

# Outputs

The engine automatically generates:

- Portfolio Equity Curve
- Spread Visualization
- Rolling Z-Score Chart
- Performance Statistics
- Trade Log (CSV)
- Parameter Optimization Report (CSV)

Performance metrics include:

- Total Return
- Annual Return
- Annual Volatility
- Sharpe Ratio
- Calmar Ratio
- Profit Factor
- Maximum Drawdown
- Win Rate

---

# Future Improvements

- Multi-pair portfolio management
- Walk-forward optimization
- Bayesian optimization
- Monte Carlo simulation
- Kalman Filter hedge ratio estimation
- Advanced portfolio risk management
- Slippage and market impact modeling
- Machine Learning signal generation
- Interactive dashboard

---

# License

This project is released under the **MIT License**.

---

# Author

**Abderrahmane**

Aspiring Quantitative Researcher | Quantitative Finance | Python | Algorithmic Trading