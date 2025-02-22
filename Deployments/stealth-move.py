import time
import numpy as np
import pandas as pd

class StealthMovementDetection:
    def __init__(self, threshold=200000, window_size=20, anomaly_factor=1.5):
        """
        Initializes the Stealth Movement Detection system.
        :param threshold: Minimum transaction value considered significant.
        :param window_size: Number of transactions to analyze for concealed accumulation.
        :param anomaly_factor: Multiplier for detecting outlier transactions.
        """
        self.threshold = threshold
        self.window_size = window_size
        self.anomaly_factor = anomaly_factor
        self.transaction_history = []
    
    def ingest_transaction(self, transaction):
        """
        Ingests a new transaction into the system.
        :param transaction: A dictionary containing 'wallet', 'amount', and 'timestamp'.
        """
        self.transaction_history.append(transaction)
        if len(self.transaction_history) > self.window_size:
            self.transaction_history.pop(0)
    
    def detect_stealth_accumulation(self):
        """
        Detects stealth accumulation patterns based on transaction history.
        :return: A dictionary with detected patterns and analysis.
        """
        df = pd.DataFrame(self.transaction_history)
        if df.empty:
            return {"status": "No transactions available for analysis."}
        
        rolling_avg = df['amount'].rolling(window=self.window_size, min_periods=1).mean()
        anomalies = df[df['amount'] > (rolling_avg * self.anomaly_factor)]
        stealth_detected = len(anomalies) > 0
        
        return {
            "stealth_accumulation_detected": stealth_detected,
            "total_anomalous_transactions": len(anomalies),
            "latest_transactions": df.tail(5).to_dict(orient='records')
        }
    
    def analyze_wallet_activity(self, wallet_address):
        """
        Analyzes a specific wallet's transaction history for concealed movements.
        :param wallet_address: Wallet address to analyze.
        :return: Analysis report.
        """
        df = pd.DataFrame(self.transaction_history)
        if df.empty:
            return {"status": "No transactions available for analysis."}
        
        wallet_transactions = df[df['wallet'] == wallet_address]
        total_value = wallet_transactions['amount'].sum()
        avg_value = wallet_transactions['amount'].mean() if not wallet_transactions.empty else 0
        
        return {
            "wallet": wallet_address,
            "total_transactions": len(wallet_transactions),
            "total_value": total_value,
            "average_transaction_value": avg_value
        }

# Example Usage
if __name__ == "__main__":
    stealth_detector = StealthMovementDetection(threshold=150000, window_size=25, anomaly_factor=2.0)
    
    sample_transactions = [
        {"wallet": "0xABC", "amount": 180000, "timestamp": time.time()},
        {"wallet": "0xDEF", "amount": 90000, "timestamp": time.time()},
        {"wallet": "0xABC", "amount": 220000, "timestamp": time.time()},
        {"wallet": "0xXYZ", "amount": 160000, "timestamp": time.time()},
        {"wallet": "0xABC", "amount": 500000, "timestamp": time.time()},
    ]
    
    for tx in sample_transactions:
        stealth_detector.ingest_transaction(tx)
    
    print(stealth_detector.detect_stealth_accumulation())
    print(stealth_detector.analyze_wallet_activity("0xABC"))
