import numpy as np
import gc

class ContinuityCalculator:
    def __init__(self):
        self.previous_signals = {}
        
    def check_continuity(self, symbol, current_signal):
        """Check if signal should be extended"""
        if symbol in self.previous_signals:
            prev = self.previous_signals[symbol]
            
            # Same direction check
            if prev['direction'] == current_signal['direction']:
                duration = min(1.8, prev.get('duration', 1.0) + 0.2)
                return {'extend': True, 'duration': duration}
        
        self.previous_signals[symbol] = current_signal
        return {'extend': False}
    
    def cleanup(self):
        """Remove old signals to save memory"""
        keys = list(self.previous_signals.keys())
        if len(keys) > 10:
            for key in keys[:-10]:
                del self.previous_signals[key]
        gc.collect()
