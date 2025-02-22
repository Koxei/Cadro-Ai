import time
import psutil
import random

# Simulated performance metrics storage
performance_metrics = {
    "latency": [],
    "throughput": [],
    "memory_usage": []
}

# Function to simulate transaction processing latency
def measure_latency():
    start_time = time.time()
    time.sleep(random.uniform(0.01, 0.1))  # Simulated processing time
    end_time = time.time()
    latency = end_time - start_time
    performance_metrics["latency"].append(latency)
    return latency

# Function to simulate throughput measurement
def measure_throughput(transactions_processed, time_interval):
    throughput = transactions_processed / time_interval
    performance_metrics["throughput"].append(throughput)
    return throughput

# Function to measure current memory usage
def measure_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    performance_metrics["memory_usage"].append(memory_usage)
    return memory_usage

# Simulated performance monitoring loop
def monitor_performance(iterations=10):
    for _ in range(iterations):
        latency = measure_latency()
        throughput = measure_throughput(random.randint(50, 200), 1)
        memory_usage = measure_memory_usage()
        
        print(f"Latency: {latency:.5f}s, Throughput: {throughput:.2f} tx/s, Memory Usage: {memory_usage:.2f}%")
        time.sleep(1)  # Simulate real-time monitoring delay

if __name__ == "__main__":
    monitor_performance()
