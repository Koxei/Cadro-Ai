import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Attention
from tensorflow.keras.optimizers import Adam

# Generate synthetic time series data
def generate_data(sequence_length=50, num_samples=1000):
    X = np.random.randn(num_samples, sequence_length, 1)
    y = np.random.randn(num_samples, 1)  # Target variable
    return X, y

# Build LSTM model with attention mechanism
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Attention(),  # Applying attention for enhanced feature extraction
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dense(1, activation='linear')  # Output layer for regression
    ])
    
    model.compile(loss='mse', optimizer=Adam(learning_rate=0.001), metrics=['mae'])
    return model

# Main execution
def main():
    X, y = generate_data()
    model = build_lstm_model(X.shape[1:])
    model.summary()
    
    # Train model (for demonstration, using limited epochs)
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

if __name__ == "__main__":
    main()
