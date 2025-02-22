import time
import numpy as np
import pandas as pd

class DistributionPhaseAnalysis:
    def __init__(self, threshold=500000, window_size=10):
        """
        Initializes the Distribution Phase Analysis system.
        :param threshold: Minimum transaction value considered significant for distribution.
        :param window_size: Number of transactions to analyze for distribution trends.
        """
        self.threshold = threshold
        self.window_size = window_size
        self.transaction_history = []
    
    def ingest_transaction(self, transaction):
        """
        Ingests a new transaction into the system.
        :param transaction: A dictionary containing 'wallet', 'amount', and 'timestamp'.
        """
        self.transaction_history.append(transaction)
        if len(self.transaction_history) > self.window_size:
            self.transaction_history.pop(0)
    
    def detect_distribution_pattern(self):
        """
        Detects distribution patterns based on transaction history.
        :return: A dictionary with detected patterns and analysis.
        """
        df = pd.DataFrame(self.transaction_history)
        if df.empty:
            return {"status": "No transactions available for analysis."}
        
        significant_transactions = df[df['amount'] >= self.threshold]
        distribution_detected = False
        
        if len(significant_transactions) >= self.window_size // 2:
            distribution_detected = True
        
        return {
            "distribution_detected": distribution_detected,
            "total_significant_transactions": len(significant_transactions),
            "latest_transactions": df.tail(5).to_dict(orient='records')
        }
    
    def analyze_wallet_distribution(self, wallet_address):
        """
        Analyzes a specific wallet's activity for potential distribution behavior.
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
    distribution_analyzer = DistributionPhaseAnalysis(threshold=300000, window_size=15)
    
    sample_transactions = [
        {"wallet": "0xABC", "amount": 400000, "timestamp": time.time()},
        {"wallet": "0xDEF", "amount": 100000, "timestamp": time.time()},
        {"wallet": "0xABC", "amount": 500000, "timestamp": time.time()},
        {"wallet": "0xXYZ", "amount": 250000, "timestamp": time.time()},
        {"wallet": "0xABC", "amount": 600000, "timestamp": time.time()},
    ]
    
    for tx in sample_transactions:
        distribution_analyzer.ingest_transaction(tx)
    
    print(distribution_analyzer.detect_distribution_pattern())
    print(distribution_analyzer.analyze_wallet_distribution("0xABC"))
