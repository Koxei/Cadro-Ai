import numpy as np

class RiskAssessmentSystem:
    def __init__(self, data, scoring_models, thresholds=None):
        """
        Initializes the Risk Assessment System.

        :param data: Input data for risk scoring (list or numpy array).
        :param scoring_models: List of risk scoring models.
        :param thresholds: Optional thresholds for each model (if applicable).
        """
        self.data = np.array(data)
        self.scoring_models = scoring_models
        self.thresholds = thresholds if thresholds else [0.5] * len(scoring_models)

    def apply_scoring_model(self, model, data):
        """
        Applies a scoring model to the input data.

        :param model: Scoring model to apply.
        :param data: Data on which the model should be applied.
        :return: Risk score calculated by the model.
        """
        return model(data)

    def assess_risk(self):
        """
        Applies all scoring models to the input data and assesses the risk.

        :return: List of risk scores for each model, with binary risk assessment (high/low) based on thresholds.
        """
        risk_scores = []
        
        for model, threshold in zip(self.scoring_models, self.thresholds):
            score = self.apply_scoring_model(model, self.data)
            # Classify the risk based on threshold (0: Low, 1: High)
            risk_class = np.where(score >= threshold, 1, 0)
            risk_scores.append((score, risk_class))
        
        return risk_scores

    def compute_comprehensive_risk(self, risk_scores):
        """
        Computes a comprehensive risk score by aggregating the individual risk scores.

        :param risk_scores: List of risk scores.
        :return: Comprehensive risk score.
        """
        # Here we take a simple weighted average for aggregation
        weighted_scores = np.array([score[0] for score in risk_scores])
        weights = np.array([0.33, 0.33, 0.34])  # Example weights for 3 models
        
        # Normalize weights if needed
        weights /= weights.sum()
        
        comprehensive_risk = np.dot(weighted_scores.T, weights)
        return comprehensive_risk

    def assess_final_risk(self, comprehensive_risk):
        """
        Assesses the final risk based on the comprehensive risk score.

        :param comprehensive_risk: The aggregated comprehensive risk score.
        :return: Final risk classification (0: Low, 1: High).
        """
        # Simple binary classification based on risk threshold
        threshold = 0.6  # Assume a threshold for final classification
        return 1 if comprehensive_risk >= threshold else 0

# Risk scoring models (example scoring algorithms)
def probabilistic_model(data):
    """
    A probabilistic model that calculates risk as a sigmoid of the data.
    The higher the value, the higher the risk.
    """
    return 1 / (1 + np.exp(-data))

def threshold_model(data):
    """
    A threshold-based model that classifies risk based on a predefined threshold.
    If data exceeds 0.5, it is considered high risk.
    """
    return np.where(data > 0.5, 1, 0)

def factorial_model(data):
    """
    A model that computes the factorial-based risk score.
    This is just an example of how more sophisticated algorithms can be used.
    """
    return np.factorial(np.clip(data, 0, 5))  # Ensure data stays within range for factorial computation

# Example usage

# Input data (e.g., risk factors or raw scores)
data = [0.2, 0.4, 0.6, 0.8]

# Define the risk scoring models
scoring_models = [probabilistic_model, threshold_model, factorial_model]

# Initialize the Risk Assessment System
assessment_system = RiskAssessmentSystem(data, scoring_models)

# Assess the risk
risk_scores = assessment_system.assess_risk()

# Compute comprehensive risk score (aggregation of individual models)
comprehensive_risk = assessment_system.compute_comprehensive_risk(risk_scores)

# Assess final risk based on the comprehensive risk score
final_risk = assessment_system.assess_final_risk(comprehensive_risk)

# Output results
print("Individual Risk Scores and Classifications (0: Low, 1: High):")
for model, (score, classification) in zip(scoring_models, risk_scores):
    print(f"Model {model.__name__}: Score = {score}, Classification = {classification}")

print(f"\nComprehensive Risk Score: {comprehensive_risk}")
print(f"Final Risk Classification (0: Low, 1: High): {final_risk}")
