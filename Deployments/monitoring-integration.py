import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import time

class PerformanceCharacteristics:
    def __init__(self, true_labels, predicted_labels, predicted_probs=None):
        """
        Initializes the Performance Characteristics class.

        :param true_labels: Ground truth labels (actual values).
        :param predicted_labels: Model's predicted labels.
        :param predicted_probs: Model's predicted probabilities (needed for AUC-ROC).
        """
        self.true_labels = np.array(true_labels)
        self.predicted_labels = np.array(predicted_labels)
        self.predicted_probs = np.array(predicted_probs) if predicted_probs is not None else None
        
    def calculate_accuracy(self):
        """
        Calculates the accuracy of the model.
        
        :return: Accuracy score.
        """
        return accuracy_score(self.true_labels, self.predicted_labels)

    def calculate_precision(self):
        """
        Calculates the precision of the model.
        
        :return: Precision score.
        """
        return precision_score(self.true_labels, self.predicted_labels)

    def calculate_recall(self):
        """
        Calculates the recall of the model.
        
        :return: Recall score.
        """
        return recall_score(self.true_labels, self.predicted_labels)

    def calculate_f1_score(self):
        """
        Calculates the F1-Score of the model.
        
        :return: F1-score.
        """
        return f1_score(self.true_labels, self.predicted_labels)

    def calculate_auc_roc(self):
        """
        Calculates the Area Under the ROC Curve (AUC-ROC) if probabilities are provided.
        
        :return: AUC-ROC score or None if probabilities are not available.
        """
        if self.predicted_probs is not None:
            return roc_auc_score(self.true_labels, self.predicted_probs)
        else:
            print("AUC-ROC cannot be calculated because predicted probabilities are missing.")
            return None

    def confusion_matrix_summary(self):
        """
        Generates and returns a confusion matrix summary (True Positives, False Positives, etc.).
        
        :return: Confusion matrix.
        """
        return confusion_matrix(self.true_labels, self.predicted_labels)

    def performance_summary(self):
        """
        Generates a summary of the performance characteristics.
        
        :return: A dictionary containing performance metrics.
        """
        accuracy = self.calculate_accuracy()
        precision = self.calculate_precision()
        recall = self.calculate_recall()
        f1 = self.calculate_f1_score()
        auc_roc = self.calculate_auc_roc()
        conf_matrix = self.confusion_matrix_summary()

        summary = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'AUC-ROC': auc_roc,
            'Confusion Matrix': conf_matrix
        }

        return summary

    def execute_with_time(self, model_function, *args):
        """
        Executes the model function and measures the execution time.
        
        :param model_function: The function of the model to be executed.
        :param args: Arguments for the model function.
        :return: Execution time and model results.
        """
        start_time = time.time()
        result = model_function(*args)
        end_time = time.time()

        execution_time = end_time - start_time
        return execution_time, result

# Example usage

# Ground truth labels (true labels)
true_labels = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

# Predicted labels (model's output after classification)
predicted_labels = [1, 0, 1, 0, 0, 1, 0, 1, 0, 1]

# Predicted probabilities (for AUC-ROC calculation)
predicted_probs = [0.9, 0.1, 0.85, 0.7, 0.2, 0.95, 0.3, 0.8, 0.4, 0.6]

# Initialize the Performance Characteristics class
performance = PerformanceCharacteristics(true_labels, predicted_labels, predicted_probs)

# Generate performance summary
summary = performance.performance_summary()

# Print performance metrics
print("Performance Metrics:")
for metric, value in summary.items():
    if metric != 'Confusion Matrix':
        print(f"{metric}: {value}")
    else:
        print(f"{metric}:\n{value}")

# Measure execution time of a hypothetical model function
def model_function(*args):
    # Simulate model execution (dummy function)
    time.sleep(2)
    return "Model executed successfully."

execution_time, result = performance.execute_with_time(model_function)
print(f"\nModel Execution Time: {execution_time:.4f} seconds")
print(f"Model Result: {result}")
