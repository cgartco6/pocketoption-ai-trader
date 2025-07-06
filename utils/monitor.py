import psutil
import time
import gc
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        
    def get_status(self):
        """Get system status summary"""
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        
        return {
            'memory_used': f"{mem.used/1024/1024:.1f} MB",
            'memory_percent': f"{mem.percent}%",
            'cpu_usage': f"{cpu}%",
            'uptime': str(timedelta(seconds=time.time()-self.start_time)),
            'time': datetime.now().strftime('%H:%M:%S')
        }
    
    def check_resources(self):
        """Check if system has enough resources"""
        mem = psutil.virtual_memory()
        if mem.percent > 85:
            gc.collect()
            return False
        return True
    
    def print_dashboard(self, stats):
        """Console dashboard"""
        status = self.get_status()
        print("\n" + "="*40)
        print(f"System Status | {status['time']}")
        print(f"Memory: {status['memory_used']} ({status['memory_percent']})")
        print(f"CPU: {status['cpu_usage']} | Uptime: {status['uptime']}")
        print("-"*40)
        print(f"Signals Today: {stats.get('green',0)}G {stats.get('red',0)}R")
        print(f"Accuracy: {self._calculate_accuracy(stats):.1f}%")
        print("="*40)
    
    def _calculate_accuracy(self, stats):
        try:
            return stats['green'] / (stats['green'] + stats['red']) * 100
        except:
            return 0.0
