import psutil
import time


def monitor_system():
    cpu_usage = psutil.cpu_percent(interval=1)
    net_io = psutil.net_io_counters()
    time.sleep(1)
    return {'cpu_usage': cpu_usage, 'net_io': net_io}