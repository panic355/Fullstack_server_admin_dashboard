from flask import Flask, jsonify
from flask_cors import CORS

from service_collector import get_systemd_services
from log_collector import returnlogs
from system_collector import returnSystemInfo
import json 

app = Flask(__name__)
CORS(app)

@app.route('/general/logs')
def general_logs():
    return jsonify(returnlogs())

@app.route('/general/services')
def general_services():
    return jsonify(get_systemd_services())

@app.route('/general/dashboard')
def general_dashboard():
    logs = {'logs': returnlogs()}
    services = {'services': get_systemd_services()}
    return jsonify(logs, services)

@app.route('/general/system')
def general_system():
    return jsonify(returnSystemInfo())


if __name__ == '__main__':
    app.run(port=(5001))
