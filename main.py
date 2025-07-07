import time
import gc
from core.signal_generator import SignalGenerator
from core.validator import SignalValidator
from core.continuity import ContinuityCalculator
from utils.reporter import TelegramReporter
from utils.monitor import SystemMonitor

def load_config():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    monitor = SystemMonitor()
    reporter = TelegramReporter(
        config['telegram']['token'],
        config['telegram']['chat_id'])
    
    sg = SignalGenerator()
    sv = SignalValidator()
    cc = ContinuityCalculator()
    
    stats = {'green': 0, 'red': 0}
    
    while True:
        if not monitor.check_resources():
            print("Waiting for memory to free up...")
            time.sleep(10)
            continue
            
        try:
            # Mock market data - replace with real API calls
            market_data = {
                "EUR/USD": {
                    "open": [1.08]*30,
                    "high": [1.09]*30,
                    "low": [1.07]*30,
                    "close": [1.085]*30,
                    "volume": [1000]*30
                }
            }
            
            signals = sg.generate_signals(market_data)
            
            for signal in signals:
                if sv.validate(signal, market_data):
                    # Check continuity
                    continuity = cc.check_continuity(
                        signal['symbol'], signal)
                    
                    if continuity['extend']:
                        signal['duration'] = continuity['duration']
                    
                    if reporter.send_signal(signal):
                        print(f"Sent signal for {signal['symbol']}")
            
            monitor.print_dashboard(stats)
            cc.cleanup()
            time.sleep(config['settings']['refresh_interval'])
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(5)
            
if __name__ == "__main__":
    main()
