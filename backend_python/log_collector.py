import subprocess
from datetime import datetime
import time
import psutil
import time

logs = []

def collect_and_print_systemd_logs(service, severity='INFO', since=None):

    # Build the journalctl command
    cmd = [
        'journalctl',
        f'UNIT={service}',
        '--output=json',
    ]

    # Run the command and capture the output
    try:
        output = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error collecting logs for {service}: {e}")
        return

    # Parse JSON output and print logs to console
    for line in output.strip().split('\n'):
        log_entry = {
            'timestamp': datetime.now(),
            'service': service,
            'log_message': line,
            'severity': severity,
        }
        return log_entry


def get_systemd_services():
        try:
            # Run the Bash command to get systemd service names using subprocess.Popen
            process = subprocess.Popen(['systemctl', 'list-units', '--type=service', '--all', '--plain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
            # Capture the standard output and error
            output, error = process.communicate()

            # Check if the process returned without errors
            if process.returncode == 0:
            # Use splitlines() to get a list of service names, excluding lines with filler text
                service_names = [line.split()[0] for line in output.strip().splitlines() if '.' in line]
                for x in range(5):
                    service_names.pop()
                return service_names
            else:
                print(f"Error getting systemd service names: {error}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def returnlogs():
    services = get_systemd_services()
    if services:
        for service in services:
            logs.append(collect_and_print_systemd_logs(service))
        return addID(logs)

def addID(logs):
    for i, log in enumerate(logs):
        log['id'] = i + 1
    return logs

