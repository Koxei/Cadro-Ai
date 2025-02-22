from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalysisEngine:
    def __init__(self, model_name='distilbert-base-uncased-finetuned-sst-2-english'):
        """
        Initializes the Sentiment Analysis Engine with a transformer model.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.pipeline = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
    
    def preprocess(self, text):
        """
        Preprocess input text: trimming, lowercasing, and tokenization.
        """
        text = text.strip().lower()
        return text
    
    def analyze_sentiment(self, text):
        """
        Perform sentiment analysis on the input text.
        """
        processed_text = self.preprocess(text)
        result = self.pipeline(processed_text)
        return result

# Example Usage
if __name__ == "__main__":
    sentiment_engine = SentimentAnalysisEngine()
    sample_text = "I love using transformer models for NLP!"
    result = sentiment_engine.analyze_sentiment(sample_text)
    print(result)
