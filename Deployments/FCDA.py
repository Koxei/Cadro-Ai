import numpy as np
import pandas as pd
import scipy.stats as stats
from arch import arch_model
import time
from prometheus_client import start_http_server, Summary, Gauge, Counter

# Performance Metrics
execution_time = Summary('flash_crash_detection_execution_seconds', 'Time spent in flash crash detection')
detected_crashes = Counter('detected_flash_crashes', 'Number of detected flash crashes')
true_positives = Counter('true_positive_flash_crashes', 'True positive flash crash detections')
false_positives = Counter('false_positive_flash_crashes', 'False positive flash crash detections')

# Parkinson's Volatility (Parametric Method)
def parkinson_volatility(high_prices, low_prices):
    log_ratios = np.log(high_prices / low_prices)
    return np.sqrt((1 / (4 * np.log(2))) * np.mean(log_ratios**2))

# GARCH Model (Parametric Method)
def garch_volatility(returns):
    model = arch_model(returns, vol='Garch', p=1, q=1)
    res = model.fit(disp='off')
    return res.conditional_volatility

# Kernel Density Estimation (Non-Parametric Method)
def kde_volatility_estimation(returns, bandwidth=0.1):
    kde = stats.gaussian_kde(returns, bw_method=bandwidth)
    return kde

# Flash Crash Detection Algorithm with Detection Parameters
@execution_time.time()
def flash_crash_detection(prices, threshold=0.05, look_back_period=5, volatility_threshold=0.02, true_crash_points=None):
    # Calculate returns
    returns = np.diff(prices) / prices[:-1]
    
    # Simulated high and low prices
    high_prices = prices[:-1] * (1 + returns)
    low_prices = prices[:-1] * (1 - returns)
    
    # Volatility Calculations
    parkinson_vol = parkinson_volatility(high_prices, low_prices)
    garch_vol = garch_volatility(returns)
    
    # Detect flash crash points based on price drop threshold
    crash_points = np.where(returns < -threshold)[0]
    
    # Filter crashes by volatility threshold (using Parkinson's and GARCH volatilities)
    crash_points_filtered = [i for i in crash_points if (parkinson_vol > volatility_threshold or garch_vol[i] > volatility_threshold)]
    
    # Metrics for performance evaluation
    detected_crashes.inc(len(crash_points_filtered))
    
    if true_crash_points is not None:
        # Compare detected crashes with true crash points
        tp = len(set(crash_points_filtered).intersection(set(true_crash_points)))
        fp = len(set(crash_points_filtered) - set(true_crash_points))
        
        true_positives.inc(tp)
        false_positives.inc(fp)
    
    return crash_points_filtered, parkinson_vol, garch_vol

# Example usage with synthetic data
def main():
    # Start Prometheus server on port 8000
    start_http_server(8000)
    
    # Simulated data generation
    np.random.seed(42)  # Ensure reproducibility
    returns = np.random.randn(50) * 0.02  # Simulated log returns
    prices = np.cumsum(returns) + 100  # Simulated price movements
    
    # Detection Parameters
    threshold = 0.05           # Threshold for flash crash drop (5%)
    volatility_threshold = 0.02  # Threshold for volatility to filter out noise
    
    # Simulate true flash crashes (example, set crash points manually for evaluation)
    true_crash_points = [10, 20, 30]  # Example true crash points
    
    crash_points, parkinson_vol, garch_vol = flash_crash_detection(prices, threshold, volatility_threshold=true_crash_threshold, true_crash_points=true_crash_points)
    
    # Output Results
    print(f"Detected Flash Crash Points (Indexes): {crash_points}")
    print(f"Parkinson's Volatility: {parkinson_vol:.5f}")
    print(f"GARCH Volatility (Last 5 values):\n {garch_vol[-5:]}")
    
    # Showing a few sampled volatility estimates from KDE
    kde = kde_volatility_estimation(returns)
    print("KDE Volatility Estimation (Sampled Values):", kde.resample(5)[0])

if __name__ == "__main__":
    main()
