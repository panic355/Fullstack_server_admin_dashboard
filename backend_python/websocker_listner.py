from flask import Flask, jsonify
import psutil
import time
from threading import Thread
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = {
    "cpu_usage": 0,
    "net_io_sent": 0,
    "net_io_recv": 0
}

previous_net_io = psutil.net_io_counters()

def bytes_to_mb(bytes):
    return bytes / (1024 * 1024)

def update_data():
    global data, previous_net_io
    while True:
        # Get CPU usage
        data['value'] = psutil.cpu_percent(interval=1)
        data['unit'] = "%"
        # Get current network I/O statistics
        current_net_io = psutil.net_io_counters()
        
        # Calculate the amount of data transmitted in this interval
        net_io_sent = bytes_to_mb(current_net_io.bytes_sent - previous_net_io.bytes_sent)
        net_io_recv = bytes_to_mb(current_net_io.bytes_recv - previous_net_io.bytes_recv)
        
        data['net_io_sent'] = net_io_sent
        data['net_io_recv'] = net_io_recv
        
        # Update previous values
        previous_net_io = current_net_io

        
        time.sleep(1)

@app.route('/data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    Thread(target=update_data).start()
    app.run(port=6789)