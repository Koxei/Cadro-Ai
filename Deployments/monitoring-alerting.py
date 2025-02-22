from prometheus_client import start_http_server, Summary, Gauge, Counter
import time
import random
import psutil

# Define Prometheus metrics
REQUEST_LATENCY = Summary('transaction_processing_latency_seconds', 'Time spent processing transactions')
THROUGHPUT = Counter('transactions_processed_total', 'Total number of transactions processed')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage of the system')
ALERT_TRIGGERED = Counter('alerts_triggered_total', 'Total number of alerts triggered')

# Simulated transaction processing function
@REQUEST_LATENCY.time()
def process_transaction():
    time.sleep(random.uniform(0.01, 0.1))  # Simulated processing delay
    THROUGHPUT.inc()

# Function to monitor system metrics
def monitor_system():
    while True:
        MEMORY_USAGE.set(psutil.virtual_memory().percent)
        if MEMORY_USAGE._value.get() > 80:  # Example alert threshold
            ALERT_TRIGGERED.inc()
            print("[ALERT] High memory usage detected!")
        time.sleep(1)

# Start Prometheus metrics server
def main():
    start_http_server(8000)  # Expose metrics at http://localhost:8000
    print("Prometheus metrics available at http://localhost:8000")
    
    # Start system monitoring
    while True:
        process_transaction()
        monitor_system()
        time.sleep(1)

if __name__ == "__main__":
    main()
