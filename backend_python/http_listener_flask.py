from flask import Flask, jsonify, request
from flask_cors import CORS


from service_collector import get_systemd_services
from log_collector import returnlogs
from system_collector import returnSystemInfo
from user_collector import get_users
from kvm_manager import list_vms, start_vm, stop_vm, destroy_vm, delete_vm
from authentication import check_sudo_password
from ssh_controller import SSHClient
import json 



# Dictionary to store SSH clients based on session or user
ssh_clients = SSHClient()

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

@app.route('/general/accounts')
def general_accounts():
    return jsonify(get_users())

@app.route('/general/vms', methods=['GET'])
def list_vms():
    vms = list_vms()
    return jsonify(vms)

@app.route('/general/vms/<vm_name>/start', methods=['POST'])
def start_vm(vm_name):
    response, status_code = start_vm(vm_name)
    return jsonify(response), status_code

@app.route('/general/vms/<vm_name>/stop', methods=['POST'])
def stop_vm(vm_name):
    response, status_code = stop_vm(vm_name)
    return jsonify(response), status_code

@app.route('/general/vms/<vm_name>/destroy', methods=['POST'])
def destroy_vm(vm_name):
    response, status_code = destroy_vm(vm_name)
    return jsonify(response), status_code

@app.route('/general/vms/<vm_name>', methods=['DELETE'])
def delete_vm(vm_name):
    response, status_code = delete_vm(vm_name)
    return jsonify(response), status_code

@app.route('/general/authenticate', methods=['POST'])
def authenticate_sudo():
    data = request.json
    if 'password' not in data:
        return jsonify({'success': False, 'message': 'No password provided'}), 400
    
    password = data['password']
    
    if check_sudo_password(password):
        return jsonify({'success': True, 'message': 'Authenticated successfully'}), 200
    else:
        return jsonify({'success': False, 'message': 'Authentication failed'}), 401


@app.route('/ssh/connect', methods=['POST'])
def connect():
    data = request.get_json()

    host = data.get('host')
    username = data.get('username')
    password = data.get('password')

    success, error = ssh_clients.connect(host, username, password)
    if success:
        return jsonify(success=True)
    else:
        return jsonify(success=False, error=error)

@app.route('/ssh/execute', methods=['POST'])
def execute():
    data = request.get_json()
    command = data.get('command')

    output = ssh_clients.execute_command(command)
    return jsonify(output=output)

@app.route('/ssh/disconnect', methods=['POST'])
def disconnect():
    ssh_clients.close_connection()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(port=(5001))
