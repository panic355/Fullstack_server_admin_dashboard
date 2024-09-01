from flask import Blueprint, jsonify
import psutil

# Define a blueprint for system management
system_management_bp = Blueprint('system_management', __name__)

@system_management_bp.route('/system/stats', methods=['GET'])
def get_system_stats():
    # Logic to fetch system statistics like CPU, RAM, etc.
    cpu_load = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    net_io = psutil.net_io_counters()


    return jsonify({
        "cpu_load": cpu_load,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
        'net_io': net_io
    })