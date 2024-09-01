from flask import Blueprint, request, jsonify
import pwd
import grp
import subprocess


# Define a blueprint for account management
account_management_bp = Blueprint('account_management', __name__)

@account_management_bp.route('/account/getall', methods=['GET'])
def get_accounts():
    
    users = []
    
    for user in pwd.getpwall():
        # Skip system users with UID below 1000 (typically)
        if user.pw_uid < 1000:
            continue

        uid = user.pw_uid
        username = user.pw_name
        full_name = user.pw_gecos.split(',')[0]
        description = user.pw_gecos
        groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]

        user_info = {
            'uid': uid,
            'username': username,
            'full_name': full_name,
            'description': description,
            'groups': groups
        }

        users.append(user_info)

    # Get accounts
    return jsonify(users)

@account_management_bp.route('/account/<string:username>', methods=['GET'])
def get_account(username):
    """
    Endpoint to get a specific account by username using the pwd module.
    """
    try:
        # Retrieve the user's information from the Unix password database
        user_info = pwd.getpwnam(username)

        # Format the response to return user details
        account = {
            "username": user_info.pw_name,
            "user_id": user_info.pw_uid,
            "group_id": user_info.pw_gid,
            "home_directory": user_info.pw_dir,
            "shell": user_info.pw_shell,
            "full_name": user_info.pw_gecos
        }
        
        return jsonify(account), 200
    
    except KeyError:
        # If the user is not found, return a 404 response
        return jsonify({"error": "Account not found"}), 404

@account_management_bp.route('/account/delete/<string:username>', methods=['DELETE'])
def delete_account(username):
    """
    Endpoint to delete a user account.
    """
    try:
        # Check if the username exists
        pwd.getpwnam(username)
    except KeyError:
        # If the user is not found, return a 404 response
        return jsonify({"error": "Account not found"}), 404

    try:
        # Delete the user account using the 'userdel' command
        result = subprocess.run(
            ['sudo', 'userdel', '-r', username],  # '-r' flag removes the home directory
            capture_output=True,
            text=True
        )

        # Check if the userdel command succeeded
        if result.returncode == 0:
            return jsonify({"message": "Account deleted successfully"}), 200
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_management_bp.route('/account/create', methods=['POST'])
def create_account():
    """
    Endpoint to create a new user account.
    """
    data = request.json
    username = data.get('username')
    shell = data.get('shell', '/bin/bash')
    home_directory = data.get('home_directory', f'/home/{username}')
    full_name = data.get('full_name', '')

    # Check if the username already exists
    try:
        pwd.getpwnam(username)
        return jsonify({"error": "Account already exists"}), 400
    except KeyError:
        # Username is available
        pass

    try:
        # Create the user account using the 'useradd' command
        result = subprocess.run(
            [
                'sudo', 'useradd',
                '-m',  # Create a home directory
                '-d', home_directory,
                '-s', shell,
                '-c', full_name,
                username
            ],
            capture_output=True,
            text=True
        )

        # Check if the useradd command succeeded
        if result.returncode == 0:
            return jsonify({"message": "Account created successfully"}), 201
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500