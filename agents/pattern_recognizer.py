import talib
import numpy as np
import psutil

class PatternRecognizer:
    def __init__(self):
        self.patterns = [
            'CDLMORNINGSTAR', 'CDLEVENINGSTAR',
            'CDLHAMMER', 'CDLINVERTEDHAMMER'
        ]
    
    def recognize(self, ohlc_data):
        """Lightweight pattern recognition"""
        results = {}
        ohlc = {
            'open': np.array(ohlc_data['open'], dtype=np.float32),
            'high': np.array(ohlc_data['high'], dtype=np.float32),
            'low': np.array(ohlc_data['low'], dtype=np.float32),
            'close': np.array(ohlc_data['close'], dtype=np.float32)
        }
        
        for pattern in self.patterns[:2]:  # Only check first 2 patterns if low memory
            if psutil.virtual_memory().percent > 75:
                break
                
            try:
                func = getattr(talib, pattern)
                results[pattern] = func(**ohlc)
            except Exception as e:
                print(f"Pattern {pattern} error: {e}")
        
        return results
