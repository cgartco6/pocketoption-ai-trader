import pandas as pd
import numpy as np
import gc

class SignalValidator:
    def __init__(self):
        self.history = pd.DataFrame(columns=[
            'symbol', 'direction', 'time', 'outcome'
        ])
    
    def validate(self, signal, market_data):
        """Validate signal against multiple criteria"""
        if len(self.history) > 1000:  # Limit history size
            self.history = self.history.iloc[-500:]
            
        try:
            # Check 1: Recent performance
            recent = self.history[
                (self.history['symbol'] == signal['symbol']) & 
                (self.history['time'] > pd.Timestamp.now() - pd.Timedelta(hours=1))
            if len(recent) > 3 and recent['outcome'].mean() < 0.6:
                return False
                
            # Check 2: Volume spike
            volumes = market_data[signal['symbol']]['volume'][-10:]
            if np.mean(volumes[-3:]) < np.mean(volumes[:-3]):
                return False
                
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
        finally:
            gc.collect()
