from flask import Blueprint, request, jsonify
import subprocess
import os

# Define a blueprint for VM management
vm_management_bp = Blueprint('vm_management', __name__)

@vm_management_bp.route('/vm/check', methods=['GET'])
def check_virtualization_environment():
    """
    Endpoint to check if virtualization is enabled and necessary packages are installed.
    """
    # Check if virtualization is supported
    virtualization_supported = check_virtualization_support()
    if not virtualization_supported:
        return jsonify({"error": "Virtualization is not enabled or supported on this host."}), 400

    # Check for necessary packages
    missing_packages = check_installed_packages()
    if missing_packages:
        return jsonify({"error": "Missing necessary packages for virtualization.", "missing_packages": missing_packages}), 400

    return jsonify({"message": "Virtualization is enabled and all necessary packages are installed."}), 200

@vm_management_bp.route('/vm/create', methods=['POST'])
def create_vm():
    """
    Endpoint to create a new virtual machine.
    """
    data = request.json
    vm_name = data.get('name')
    memory = data.get('memory', '1024')  # Memory in MB
    vcpus = data.get('vcpus', '1')       # Number of CPUs
    disk_size = data.get('disk_size', '10')  # Disk size (e.g., 10G for 10 gigabytes)
    iso_path = data.get('iso_path')
    network = data.get('network', 'default')

    # Validate input data
    if not vm_name or not iso_path:
        return jsonify({"error": "Missing required fields: 'name' and 'iso_path'."}), 400

    # Command to create a new VM using virt-install
    command = [
        'sudo', 'virt-install',
        '--name', vm_name,
        '--memory', memory,
        '--vcpus', vcpus,
        '--disk', f'path=/var/lib/libvirt/images/{vm_name}.img,size={disk_size}',
        '--cdrom', iso_path,
        '--network', network,
        '--os-variant', 'generic',
        '--graphics', 'none',  # You can adjust this to suit your needs
        '--console', 'pty,target_type=serial',
        '--noautoconsole'
    ]

    try:
        # Execute the command to create the VM
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({"message": f"VM '{vm_name}' created successfully."}), 201
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vm_management_bp.route('/vm/delete', methods=['DELETE'])
def delete_vm_endpoint():
    """
    Endpoint to delete a virtual machine.
    """
    vm_name = request.json.get('name')
    if not vm_name:
        return jsonify({"error": "Missing VM name parameter."}), 400

    result = delete_vm(vm_name)
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 200

@vm_management_bp.route('/vm/start', methods=['POST'])
def start_vm():
    """
    Endpoint to start a virtual machine.
    """
    vm_name = request.json.get('name')
    if not vm_name:
        return jsonify({"error": "Missing VM name parameter."}), 400

    result = execute_virsh_command(['start', vm_name])
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 200

@vm_management_bp.route('/vm/shutdown', methods=['POST'])
def stop_vm():
    """
    Endpoint to stop a virtual machine.
    """
    vm_name = request.json.get('name')
    if not vm_name:
        return jsonify({"error": "Missing VM name parameter."}), 400

    result = execute_virsh_command(['shutdown', vm_name])
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 200

@vm_management_bp.route('/vm/restart', methods=['POST'])
def restart_vm():
    """
    Endpoint to restart a virtual machine.
    """
    vm_name = request.json.get('name')
    if not vm_name:
        return jsonify({"error": "Missing VM name parameter."}), 400

    result = execute_virsh_command(['reboot', vm_name])
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 200

@vm_management_bp.route('/vm/stop', methods=['POST'])
def shutdown_vm():
    """
    Endpoint to forcefully shutdown a virtual machine.
    """
    vm_name = request.json.get('name')
    if not vm_name:
        return jsonify({"error": "Missing VM name parameter."}), 400

    result = execute_virsh_command(['destroy', vm_name])
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 200

@vm_management_bp.route('/vm/list', methods=['GET'])
def list_vms():
    """
    Endpoint to list all virtual machines and their details.
    """
    vms = get_vm_list()
    return jsonify(vms)

def get_vm_list():
    """
    Fetch the list of all virtual machines.
    """
    try:
        # Use virsh to list VMs and get their names
        result = subprocess.run(['virsh', 'list', '--all', '--name'], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception("Error fetching VM list: " + result.stderr)

        # Split the result into lines and strip whitespace
        vm_names = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        vms = []
        for vm_name in vm_names:
            # Fetch detailed info for each VM
            info_result = subprocess.run(['virsh', 'dominfo', vm_name], capture_output=True, text=True)
            if info_result.returncode != 0:
                raise Exception(f"Error fetching info for VM '{vm_name}': " + info_result.stderr)
            
            # Parse the info
            info_lines = info_result.stdout.splitlines()
            vm_info = {}
            for line in info_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    vm_info[key.strip()] = value.strip()
            
            vm_info['name'] = vm_name
            vms.append(vm_info)

        return vms

    except Exception as e:
        return {'error': str(e)}

def delete_vm(vm_name):
    """
    Delete a virtual machine by its name.
    """
    try:
        # Command to delete the VM
        result = subprocess.run(['virsh', 'undefine', vm_name, '--remove-all-storage'], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception("Error deleting VM: " + result.stderr)

        return {"message": f"VM '{vm_name}' deleted successfully."}

    except Exception as e:
        return {"error": str(e)}

def execute_virsh_command(command_args):
    """
    Execute a virsh command and return the result.
    """
    try:
        result = subprocess.run(['virsh'] + command_args, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("Error executing command: " + result.stderr)
        return {"message": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

def check_virtualization_support():
    """
    Check if the host hardware has virtualization enabled.
    """
    try:
        # Read the CPU information from /proc/cpuinfo
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        
        # Check for Intel VT-x or AMD-V support in the CPU flags
        if "vmx" in cpuinfo or "svm" in cpuinfo:
            return True
        else:
            return False
    except Exception as e:
        return False

def detect_package_manager():
    """
    Detect the package manager used on the host system.
    """
    package_managers = {
        'apt': 'dpkg-query -W',
        'yum': 'rpm -q',
        'dnf': 'rpm -q',
        'pacman': 'pacman -Qi',
        'zypper': 'rpm -q'
    }

    for manager, check_cmd in package_managers.items():
        try:
            # Try to run the version command of each package manager
            result = subprocess.run([manager, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return manager, check_cmd
        except FileNotFoundError:
            continue

    return None, None

def check_installed_packages():
    """
    Check if necessary virtualization packages are installed dynamically based on the package manager.
    """
    necessary_packages = ['libvirt', 'qemu', 'virt-manager']
    missing_packages = []

    package_manager, check_cmd = detect_package_manager()

    if not package_manager:
        return {"error": "No supported package manager detected."}

    # Check each package using the detected package manager
    for package in necessary_packages:
        try:
            # Use the appropriate command to check for each package
            result = subprocess.run(f"{check_cmd} {package}".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:  # The package is missing
                missing_packages.append(package)
        except Exception as e:
            missing_packages.append(package)

    return missing_packages