import time
import numpy as np
import pandas as pd

class WhaleDetectionSystem:
    def __init__(self, threshold=1000000, window_size=10):
        """
        Initializes the Whale Detection System with configurable parameters.
        :param threshold: Minimum transaction value considered as whale activity.
        :param window_size: Number of transactions to analyze for pattern recognition.
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
    
    def detect_accumulation_pattern(self):
        """
        Detects accumulation patterns based on transaction history.
        :return: A dictionary with detected patterns and analysis.
        """
        df = pd.DataFrame(self.transaction_history)
        if df.empty:
            return {"status": "No transactions available for analysis."}
        
        whale_transactions = df[df['amount'] >= self.threshold]
        accumulation_detected = False
        
        if len(whale_transactions) >= self.window_size // 2:
            accumulation_detected = True
        
        return {
            "accumulation_detected": accumulation_detected,
            "total_whale_transactions": len(whale_transactions),
            "latest_transactions": df.tail(5).to_dict(orient='records')
        }
    
    def analyze_wallet_behavior(self, wallet_address):
        """
        Analyzes a specific wallet's activity for potential whale behavior.
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
    whale_detector = WhaleDetectionSystem(threshold=500000, window_size=20)
    
    sample_transactions = [
        {"wallet": "0xABC", "amount": 600000, "timestamp": time.time()},
        {"wallet": "0xDEF", "amount": 200000, "timestamp": time.time()},
        {"wallet": "0xABC", "amount": 700000, "timestamp": time.time()},
        {"wallet": "0xXYZ", "amount": 100000, "timestamp": time.time()},
        {"wallet": "0xABC", "amount": 800000, "timestamp": time.time()},
    ]
    
    for tx in sample_transactions:
        whale_detector.ingest_transaction(tx)
    
    print(whale_detector.detect_accumulation_pattern())
    print(whale_detector.analyze_wallet_behavior("0xABC"))
