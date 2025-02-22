import numpy as np
import pandas as pd
import scipy.stats as stats

# Parkinson's Volatility (Parametric Method)
def parkinson_volatility(high_prices, low_prices):
    log_ratios = np.log(high_prices / low_prices)
    return np.sqrt((1 / (4 * np.log(2))) * np.mean(log_ratios**2))

# GARCH Model (Parametric Method)
from arch import arch_model

def garch_volatility(returns):
    model = arch_model(returns, vol='Garch', p=1, q=1)
    res = model.fit(disp='off')
    return res.conditional_volatility

# Kernel Density Estimation (Non-Parametric Method)
def kde_volatility_estimation(returns, bandwidth=0.1):
    kde = stats.gaussian_kde(returns, bw_method=bandwidth)
    return kde

# Flash Crash Detection Algorithm
def flash_crash_detection(prices, threshold=0.05):
    returns = np.diff(prices) / prices[:-1]
    crash_points = np.where(returns < -threshold)[0]
    return crash_points

# Example usage with synthetic data
def main():
    high_prices = np.random.uniform(100, 200, 50)
    low_prices = np.random.uniform(90, 195, 50)
    returns = np.random.randn(50) * 0.02  # Simulated log returns
    prices = np.cumsum(returns) + 100  # Simulated price movements
    
    parkinson_vol = parkinson_volatility(high_prices, low_prices)
    garch_vol = garch_volatility(returns)
    kde = kde_volatility_estimation(returns)
    crash_points = flash_crash_detection(prices)
    
    print(f"Parkinson's Volatility: {parkinson_vol:.5f}")
    print("GARCH Volatility (Last 5 values):\n", garch_vol.tail())
    print("KDE Volatility Estimation (Sampled Values):", kde.resample(5)[0])
    print("Flash Crash Detected at Indexes:", crash_points)

if __name__ == "__main__":
    main()
