import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def fetch_live_data(ticker="CL=F"):
    """
    Fetch live spot price and estimated volatility from Yahoo Finance.
    """
    data = yf.Ticker(ticker)
    hist = data.history(period="30d")

    if hist.empty:
        raise ValueError("No historical data found. Check ticker symbol.")

    spot = hist['Close'].iloc[-1]
    returns = hist['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility

    return spot, volatility

def commodity_fdm_pricer(S_max, K, T, r, sigma, delta=0.02, M=100, N=1000, option_type="call"):
    """
    Solve Black-Scholes PDE for a commodity option using Explicit Finite Difference Method.
    """
    dS = S_max / M
    dt = T / N

    S = np.linspace(0, S_max, M+1)
    V = np.maximum(0, (S - K) if option_type == "call" else (K - S))  # Payoff at maturity

    # Time stepping
    for n in range(N):
        V_prev = V.copy()
        for i in range(1, M):
            delta_S = (r - delta) * i
            gamma_S = 0.5 * sigma**2 * i**2

            A = dt * (gamma_S - delta_S) / 2
            B = 1 - dt * (sigma**2 * i**2 + r)
            C = dt * (gamma_S + delta_S) / 2

            V[i] = A * V_prev[i-1] + B * V_prev[i] + C * V_prev[i+1]

        # Boundary conditions
        V[0] = 0
        if option_type == "call":
            V[M] = S_max - K * np.exp(-r * (n * dt))
        else:
            V[M] = 0

    return S, V

if __name__ == "__main__":
    # Parameters
    ticker = "CL=F"  # WTI Crude Oil Futures
    T = 0.5          # 6 months to maturity
    r = 0.05         # Approximate risk-free rate (can adjust)
    delta = 0.02     # Convenience yield
    option_type = "call"

    # Fetch live spot price and volatility
    spot, vol = fetch_live_data(ticker)
    print(f"Live Spot Price: {spot:.2f}")
    print(f"Estimated Volatility: {vol:.2%}")

    # Solver parameters
    S_max = 1.1 * spot  # Max price for grid
    K = spot          # ATM option
    M, N = 100, 1000  # Grid sizes

    # Price the option
    S, V = commodity_fdm_pricer(S_max, K, T, r, vol, delta, M, N, option_type)

    # Plot results
    plt.figure(figsize=(8,5))
    plt.plot(S, V, label=f"Commodity {option_type.capitalize()} Option")
    plt.xlabel("Spot Price S")
    plt.ylabel("Option Price V")
    plt.title(f"FDM Pricing - {ticker} - {option_type.capitalize()} Option")
    plt.legend()
    plt.grid(True)
    plt.savefig("examples/option_surface_plot.png", dpi=300)
    plt.show()
