import numpy as np
import pandas as pd
import scipy.stats as stats

# Parkinson's High-Low Range Volatility Calculation
def parkinson_volatility(high_prices, low_prices):
    log_ratios = np.log(high_prices / low_prices)
    return np.sqrt((1 / (4 * np.log(2))) * np.mean(log_ratios**2))

# Exponentially Weighted Moving Average (EWMA) for Volume Analysis
def ewma_volume(volume_series, alpha=0.94):
    return volume_series.ewm(alpha=alpha).mean()

# Non-Parametric Kernel Density Estimation for Liquidity Distribution
def kde_liquidity_estimation(liquidity_data, bandwidth=0.5):
    kde = stats.gaussian_kde(liquidity_data, bw_method=bandwidth)
    return kde

# Implementation example for liquidity impact calculation
def liquidity_impact(trade_volume, pool_liquidity):
    return trade_volume / (trade_volume + pool_liquidity)

# Example usage with synthetic data
def main():
    high_prices = np.random.uniform(100, 200, 50)
    low_prices = np.random.uniform(90, 195, 50)
    volume_series = pd.Series(np.random.uniform(1000, 10000, 50))
    liquidity_data = np.random.uniform(50000, 200000, 50)
    trade_volume = 1500
    pool_liquidity = 100000

    volatility = parkinson_volatility(high_prices, low_prices)
    ewma_volumes = ewma_volume(volume_series)
    kde = kde_liquidity_estimation(liquidity_data)
    liquidity_impact_value = liquidity_impact(trade_volume, pool_liquidity)

    print(f"Parkinson's Volatility: {volatility:.5f}")
    print(f"Liquidity Impact: {liquidity_impact_value:.5f}")
    print("EWMA Volume Analysis (Last 5 values):\n", ewma_volumes.tail())
    print("KDE Liquidity Estimation (Sampled Values):", kde.resample(5)[0])

if __name__ == "__main__":
    main()
