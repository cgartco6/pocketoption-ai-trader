from telegram import Bot
from telegram.error import TelegramError
import pandas as pd
import gc
import sys

class TelegramReporter:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.session_stats = {'green': 0, 'red': 0}
        self.active_signals = {}
        
    def send_signal(self, signal):
        """Send signal to Telegram"""
        try:
            msg = (
                f"🚀 *Signal* ({signal['confidence']*100:.0f}%)\n"
                f"📈 {signal['symbol']} {signal['direction']}\n"
                f"⏳ Expiry: {signal.get('duration', 1)} min\n"
                f"🕒 {signal['time'].strftime('%H:%M:%S')}"
            )
            
            self.bot.send_message(
                chat_id=self.chat_id,
                text=msg,
                parse_mode='Markdown'
            )
            
            signal_id = f"{signal['symbol']}_{signal['time'].timestamp()}"
            self.active_signals[signal_id] = signal
            self._cleanup_signals()
            return True
        except TelegramError as e:
            print(f"Telegram error: {e}")
            return False
        finally:
            gc.collect()
    
    def report_outcome(self, signal_id, success):
        """Report trade outcome"""
        try:
            if signal_id in self.active_signals:
                outcome = '✅ GREEN' if success else '❌ RED'
                self.session_stats['green' if success else 'red'] += 1
                
                msg = (
                    f"Signal {signal_id[:10]}...: {outcome}\n"
                    f"Session: {self.session_stats['green']}G | {self.session_stats['red']}R"
                )
                
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=msg
                )
                del self.active_signals[signal_id]
                return True
            return False
        except Exception as e:
            print(f"Outcome report error: {e}")
            return False
    
    def _cleanup_signals(self):
        """Cleanup old signals to save memory"""
        if sys.platform == 'win32' and len(self.active_signals) > 5:
            # Be more aggressive on Windows
            keys = sorted(self.active_signals.keys())
            for key in keys[:-5]:
                del self.active_signals[key]
        elif len(self.active_signals) > 10:
            keys = sorted(self.active_signals.keys())
            for key in keys[:-10]:
                del self.active_signals[key]
        gc.collect()
