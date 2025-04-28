# Commodity Option Pricing using Finite Difference Method (with Live Data)

This project implements an **Explicit Finite Difference Method (FDM)** to solve the **Black-Scholes PDE adapted for commodity options** — including a **convenience yield adjustment**.  
It fetches **live market data** from Yahoo Finance to simulate real-world commodity option pricing conditions.

---

## ✨ Features

- Solves the Black-Scholes PDE for European call and put options on commodities.
- Integrates **live spot price** and **historical volatility** using [`yfinance`](https://pypi.org/project/yfinance/).
- Adjusts for **convenience yield** (storage costs/benefits) — crucial in commodity markets.
- Plots option value curves dynamically based on live data.
- Automatically saves the resulting plot to the `examples/` folder.

---

## 📚 Mathematical Model

We solve the Black-Scholes PDE with convenience yield adjustment:

\[
\frac{\partial V}{\partial t} + (r - \delta) S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0
\]

Where:
- \( V \) = option value
- \( S \) = spot price of commodity
- \( r \) = risk-free interest rate
- \( \delta \) = convenience yield
- \( \sigma \) = volatility

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourgithubusername/pdesolver.git
cd pdesolver
