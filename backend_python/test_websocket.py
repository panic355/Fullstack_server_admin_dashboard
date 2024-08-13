from flask import Flask
from flask_socketio import SocketIO, emit
import psutil
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

def fetch_system_stats():
    while True:
        stats = {
            'cpu_load': psutil.cpu_percent(),
            'ram_usage': psutil.virtual_memory().percent,
            'storage_usage': psutil.disk_usage('/').percent,
            'net_io': psutil.net_io_counters()
        }
        socketio.emit('system_stats', stats)
        time.sleep(5)
 
@socketio.on('connect')
def handle_connect():
    try:
        print('Client connected')
        emit('response', {'data': 'Hello from server!'})
    except Exception as e:
        print(f'Error handling connection: {e}')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return 'WebSocket Server is running!'

if __name__ == '__main__':
    threading.Thread(target=fetch_system_stats).start()
    socketio.run(app, host='0.0.0.0', port=6969, debug=True)