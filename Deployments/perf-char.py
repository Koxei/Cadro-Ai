class PerformanceMetrics:
    def __init__(self):
        """
        Initializes the Performance Metrics tracker.
        """
        self.metrics = {}
    
    def record_metric(self, metric_name, value):
        """
        Records a performance metric with a given name and value.
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)
    
    def get_average(self, metric_name):
        """
        Computes and returns the average value for a given metric.
        """
        if metric_name in self.metrics and self.metrics[metric_name]:
            return sum(self.metrics[metric_name]) / len(self.metrics[metric_name])
        return None
    
    def report(self):
        """
        Generates a summary report of all recorded metrics.
        """
        return {metric: self.get_average(metric) for metric in self.metrics}

# Example Usage
if __name__ == "__main__":
    perf_tracker = PerformanceMetrics()
    perf_tracker.record_metric("response_time", 120)
    perf_tracker.record_metric("response_time", 150)
    perf_tracker.record_metric("cpu_usage", 75)
    perf_tracker.record_metric("cpu_usage", 80)
    
    print(perf_tracker.report())
