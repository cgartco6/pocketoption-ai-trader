import requests
import json
from textblob import TextBlob
import gc

class SentimentAnalyzer:
    def __init__(self):
        self.cache = {}
        
    def get_sentiment(self, symbol):
        """Lightweight sentiment analysis with caching"""
        if symbol in self.cache:
            return self.cache[symbol]
            
        try:
            # Simplified sentiment analysis
            news = self._fetch_news(symbol)
            analysis = TextBlob(news[:512])  # Limit text size
            sentiment = analysis.sentiment.polarity
            self.cache[symbol] = sentiment
            return sentiment
        except Exception as e:
            print(f"Sentiment error: {e}")
            return 0
        finally:
            gc.collect()
    
    def _fetch_news(self, symbol):
        """Mock news fetcher - implement your own API calls"""
        return f"Market update for {symbol}: mixed signals today"
