from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import gc
from ..agents import DeepLearningPredictor, PatternRecognizer, SentimentAnalyzer

class SignalGenerator:
    def __init__(self):
        self.dlp = DeepLearningPredictor()
        self.pr = PatternRecognizer()
        self.sa = SentimentAnalyzer()
        self.signals = []
        
    def generate_signals(self, asset_data):
        """Generate signals for multiple assets with memory management"""
        signals = []
        
        for symbol, data in asset_data.items():
            if len(signals) >= 3:  # Process max 3 assets at once
                break
                
            try:
                signal = self._process_asset(symbol, data)
                if signal:
                    signals.append(signal)
            except MemoryError:
                gc.collect()
                continue
                
        return signals
    
    def _process_asset(self, symbol, data):
        """Process single asset data"""
        # Convert to numpy float32 to save memory
        data = {k: np.array(v[-30:], dtype=np.float32) for k,v in data.items()}
        
        # Get predictions
        dl_pred = self.dlp.predict(data)
        patterns = self.pr.recognize(data)
        sentiment = self.sa.get_sentiment(symbol)
        
        # Calculate signal confidence (simplified)
        confidence = (dl_pred * 0.6 + 
                     (1 if patterns else 0) * 0.3 + 
                     (sentiment + 1)/2 * 0.1)
        
        if confidence > 0.75:
            direction = 'BUY' if dl_pred > 0.5 else 'SELL'
            return {
                'symbol': symbol,
                'direction': direction,
                'confidence': round(confidence, 2),
                'time': datetime.now(),
                'expiry': 1  # Default 1 minute
            }
        return None
