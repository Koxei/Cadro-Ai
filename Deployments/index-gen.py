import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class IndexGenerationPipeline:
    def __init__(self, data_sources, weights=None):
        """
        Initializes the Index Generation Pipeline.

        :param data_sources: List of pandas DataFrames (each representing a data source).
        :param weights: Weights to assign to each data source in the final index (if applicable).
        """
        self.data_sources = data_sources
        self.weights = weights if weights else np.ones(len(data_sources)) / len(data_sources)

        # Normalize weights to sum to 1
        self.weights = np.array(self.weights)
        self.weights /= self.weights.sum()

    def handle_missing_values(self, data):
        """
        Handles missing values by filling them with the mean value of the column.

        :param data: DataFrame with missing values.
        :return: DataFrame with missing values handled.
        """
        return data.fillna(data.mean())

    def scale_data(self, data):
        """
        Scales the data using Min-Max scaling to ensure all features are on a similar scale.
        
        :param data: DataFrame with the data to scale.
        :return: Scaled DataFrame.
        """
        scaler = MinMaxScaler()
        return pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

    def process_data(self):
        """
        Process each data source, including handling missing values and scaling the data.

        :return: List of processed DataFrames.
        """
        processed_data = []
        for data in self.data_sources:
            # Step 1: Handle missing values
            data = self.handle_missing_values(data)
            # Step 2: Scale the data
            data = self.scale_data(data)
            processed_data.append(data)
        
        return processed_data

    def calculate_index(self, processed_data):
        """
        Calculate the composite index by aggregating the weighted data sources.
        
        :param processed_data: List of processed data DataFrames.
        :return: Composite index.
        """
        # Initialize the composite index with zeros
        index = np.zeros(processed_data[0].shape[0])

        # Aggregate data sources using their weights
        for i, data in enumerate(processed_data):
            index += data.mean(axis=1) * self.weights[i]

        return index

    def validate_index(self, index):
        """
        Validates the generated index, checking for any anomalies or out-of-bound values.
        
        :param index: The generated composite index.
        :return: Boolean indicating if the index is valid.
        """
        # Check if all index values are within a valid range (0 to 1 in this case)
        if np.any(index < 0) or np.any(index > 1):
            print("Index validation failed: Values are out of bounds.")
            return False
        return True

    def generate_index(self):
        """
        Generate the composite index by processing the data and calculating the index.

        :return: The final composite index.
        """
        # Step 1: Process the data
        processed_data = self.process_data()

        # Step 2: Calculate the composite index
        composite_index = self.calculate_index(processed_data)

        # Step 3: Validate the index
        if self.validate_index(composite_index):
            return composite_index
        else:
            print("Invalid index detected.")
            return None

# Example usage

# Example DataFrames representing different data sources (e.g., economic factors, market performance)
data_source_1 = pd.DataFrame({
    'factor_1': [0.1, 0.2, 0.3, 0.4, 0.5],
    'factor_2': [0.6, 0.5, 0.4, 0.3, 0.2],
    'factor_3': [0.7, 0.6, 0.5, 0.4, 0.3]
})

data_source_2 = pd.DataFrame({
    'factor_4': [0.8, 0.7, 0.6, 0.5, 0.4],
    'factor_5': [0.3, 0.2, 0.1, 0.4, 0.5],
    'factor_6': [0.1, 0.2, 0.3, 0.4, 0.5]
})

data_source_3 = pd.DataFrame({
    'factor_7': [0.2, 0.3, 0.4, 0.5, 0.6],
    'factor_8': [0.9, 0.8, 0.7, 0.6, 0.5],
    'factor_9': [0.6, 0.5, 0.4, 0.3, 0.2]
})

# List of data sources
data_sources = [data_source_1, data_source_2, data_source_3]

# Define weights for each data source (if applicable)
weights = [0.5, 0.3, 0.2]

# Initialize the Index Generation Pipeline
index_pipeline = IndexGenerationPipeline(data_sources, weights)

# Generate the composite index
composite_index = index_pipeline.generate_index()

# Output the result
if composite_index is not None:
    print("Generated Composite Index:")
    print(composite_index)
