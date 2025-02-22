import time
import psutil
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class MonitoringIntegration:
    def __init__(self, true_labels, predicted_labels, predicted_probs=None):
        """
        Initializes the monitoring integration class with labels and predicted data.
        
        :param true_labels: Ground truth labels (actual values).
        :param predicted_labels: Model's predicted labels.
        :param predicted_probs: Model's predicted probabilities (optional, needed for AUC-ROC).
        """
        self.true_labels = np.array(true_labels)
        self.predicted_labels = np.array(predicted_labels)
        self.predicted_probs = np.array(predicted_probs) if predicted_probs is not None else None

        # Initialize system resource usage metrics
        self.cpu_usage = None
        self.memory_usage = None
        self.execution_time = None

    def calculate_model_metrics(self):
        """
        Calculates model performance metrics like accuracy, precision, recall, and F1 score.

        :return: Dictionary containing model performance metrics.
        """
        metrics = {
            'accuracy': accuracy_score(self.true_labels, self.predicted_labels),
            'precision': precision_score(self.true_labels, self.predicted_labels),
            'recall': recall_score(self.true_labels, self.predicted_labels),
            'f1_score': f1_score(self.true_labels, self.predicted_labels)
        }
        return metrics

    def get_system_metrics(self):
        """
        Retrieves system resource usage metrics such as CPU and memory usage.
        
        :return: Dictionary containing CPU and memory usage information.
        """
        self.cpu_usage = psutil.cpu_percent(interval=1)
        self.memory_usage = psutil.virtual_memory().percent
        system_metrics = {
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage
        }
        return system_metrics

    def measure_execution_time(self, model_function, *args):
        """
        Measures the execution time of a given function.

        :param model_function: Function to be executed (model inference or training).
        :param args: Arguments to be passed to the function.
        :return: Execution time in seconds.
        """
        start_time = time.time()
        model_function(*args)
        end_time = time.time()
        self.execution_time = end_time - start_time
        return self.execution_time

    def generate_metrics_report(self):
        """
        Generates a report containing both model metrics and system metrics.
        
        :return: Dictionary containing all metrics (model performance, system usage, and execution time).
        """
        model_metrics = self.calculate_model_metrics()
        system_metrics = self.get_system_metrics()
        
        # Combine model, system, and execution time metrics into one report
        report = {
            'model_metrics': model_metrics,
            'system_metrics': system_metrics,
            'execution_time': self.execution_time
        }
        
        return report

    def expose_metrics(self):
        """
        Exposes the collected metrics in a comprehensive format for monitoring purposes.
        This could be integrated with a monitoring system (e.g., Prometheus, Grafana).
        
        :return: The collected metrics as a dictionary.
        """
        metrics_report = self.generate_metrics_report()
        
        # For integration with Prometheus or a custom monitoring system, 
        # you would send these metrics to the system here.
        
        # For the sake of this example, we'll just print the report
        print("Exposing Metrics:")
        for key, value in metrics_report.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
                
        return metrics_report

# Example usage

# Example true labels and predicted labels (from a model)
true_labels = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
predicted_labels = [1, 0, 1, 0, 0, 1, 0, 1, 0, 1]
predicted_probs = [0.9, 0.1, 0.85, 0.7, 0.2, 0.95, 0.3, 0.8, 0.4, 0.6]

# Initialize the MonitoringIntegration class
monitoring = MonitoringIntegration(true_labels, predicted_labels, predicted_probs)

# Example of a dummy model function (simulating inference or training)
def dummy_model_function(*args):
    # Simulating some computation or model processing time
    time.sleep(1)

# Measure execution time of the dummy model function
execution_time = monitoring.measure_execution_time(dummy_model_function)

# Expose metrics
monitoring.expose_metrics()

# Output example might look like:
# Exposing Metrics:
# model_metrics:
#   accuracy: 0.9
#   precision: 0.9
#   recall: 1.0
#   f1_score: 0.9473684210526315
# system_metrics:
#   cpu_usage: 12.0
#   memory_usage: 75.0
# execution_time: 1.0023
