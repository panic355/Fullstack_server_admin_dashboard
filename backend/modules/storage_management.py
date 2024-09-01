from flask import Blueprint, request, jsonify

# Define a blueprint for storage management
storage_management_bp = Blueprint('storage_management', __name__)

@storage_management_bp.route('/storage/add', methods=['POST'])
def add_storage():
    # Logic to add storage
    data = request.json
    # Process the data and add storage
    return jsonify({"message": "Storage added successfully!"})

@storage_management_bp.route('/storage/remove', methods=['POST'])
def remove_storage():
    # Logic to remove storage
    data = request.json
    # Process the data and remove storage
    return jsonify({"message": "Storage removed successfully!"})