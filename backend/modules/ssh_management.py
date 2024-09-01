from flask import Blueprint, request, jsonify

# Define a blueprint for SSH management
ssh_management_bp = Blueprint('ssh_management', __name__)

@ssh_management_bp.route('/ssh/connect', methods=['POST'])
def connect_ssh():
    # Logic to connect to a server via SSH
    data = request.json
    # Process the data and establish an SSH connection
    return jsonify({"message": "Connected to SSH successfully!"})

@ssh_management_bp.route('/ssh/disconnect', methods=['POST'])
def disconnect_ssh():
    # Logic to disconnect from SSH
    return jsonify({"message": "Disconnected from SSH successfully!"})