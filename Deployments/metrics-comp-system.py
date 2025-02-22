import numpy as np

class ScoreAggregationSystem:
    def __init__(self, analysis_vectors, weights):
        """
        Initializes the Score Aggregation System.

        :param analysis_vectors: List of numpy arrays or lists of risk scores or probabilities.
        :param weights: List of weights associated with each analysis vector.
        """
        if len(analysis_vectors) != len(weights):
            raise ValueError("The number of analysis vectors must be equal to the number of weights.")
        
        self.analysis_vectors = [np.array(vec) for vec in analysis_vectors]
        self.weights = np.array(weights)
        
        # Normalize weights to sum to 1
        self.weights /= self.weights.sum()

    def aggregate_scores(self):
        """
        Aggregates the scores from multiple analysis vectors using weighted sum.

        :return: Aggregated risk score
        """
        # Perform weighted sum of analysis vectors
        aggregated_score = np.zeros_like(self.analysis_vectors[0])
        
        for vec, weight in zip(self.analysis_vectors, self.weights):
            aggregated_score += vec * weight

        return aggregated_score

    def assess_risk(self, aggregated_score):
        """
        Assesses the risk using a probabilistic model. Here, we assume a simple threshold-based risk model.

        :param aggregated_score: The aggregated risk score.
        :return: Risk assessment as a probability.
        """
        # For simplicity, let's say the higher the aggregated score, the higher the risk
        # We use a sigmoid function for probabilistic risk assessment (between 0 and 1).
        risk_probability = 1 / (1 + np.exp(-aggregated_score))
        return risk_probability

    def compute_risk_metric(self):
        """
        Compute the comprehensive risk metric by aggregating the scores and assessing the risk.

        :return: Comprehensive risk metric as a probability.
        """
        # Aggregate the scores
        aggregated_score = self.aggregate_scores()
        
        # Assess the risk using the aggregated score
        risk_metric = self.assess_risk(aggregated_score)
        
        return risk_metric


# Example usage

# Define multiple analysis vectors (these could represent different risk factors or scores)
analysis_vectors = [
    [0.2, 0.4, 0.6, 0.8],  # Risk scores from analysis 1
    [0.3, 0.5, 0.7, 0.9],  # Risk scores from analysis 2
    [0.4, 0.6, 0.8, 1.0],  # Risk scores from analysis 3
]

# Define the weights for each analysis vector (indicating the importance of each analysis)
weights = [0.5, 0.3, 0.2]

# Initialize the Score Aggregation System
aggregation_system = ScoreAggregationSystem(analysis_vectors, weights)

# Compute the comprehensive risk metric
risk_metric = aggregation_system.compute_risk_metric()

print("Comprehensive Risk Metric:", risk_metric)
