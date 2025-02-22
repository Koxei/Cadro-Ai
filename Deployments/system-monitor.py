from flask import Flask, jsonify
import psutil
import time

app = Flask(__name__)

class SystemMonitoring:
    def __init__(self):
        """
        Initializes the System Monitoring engine.
        """
        self.start_time = time.time()
    
    def get_cpu_usage(self):
        """Returns the current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self):
        """Returns the current memory usage in MB."""
        memory_info = psutil.virtual_memory()
        return memory_info.used / (1024 * 1024)
    
    def get_uptime(self):
        """Returns the system uptime in seconds."""
        return time.time() - self.start_time
    
    def get_metrics(self):
        """Returns a dictionary of system metrics."""
        return {
            "cpu_usage": self.get_cpu_usage(),
            "memory_usage_mb": self.get_memory_usage(),
            "uptime_seconds": self.get_uptime()
        }

monitor = SystemMonitoring()

@app.route("/metrics", methods=["GET"])
def metrics():
    """Exposes system monitoring metrics through a REST API endpoint."""
    return jsonify(monitor.get_metrics())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
