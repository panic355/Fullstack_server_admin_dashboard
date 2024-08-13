import json 
import subprocess
serviceList = []

# Send a ping to confirm a successful connection

def get_systemd_services():
    try:
        # Run the Bash command to get systemd service names using subprocess.Popen
        process = subprocess.Popen(['systemctl', 'list-units', '--type=service', '--all', '--plain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Capture the standard output and error
        output, error = process.communicate()

        # Check if the process returned without errors
        if process.returncode == 0:
            # Use splitlines() to get a list of service names, excluding lines with filler text
            services = output.strip().split('\n')
            services.pop(0)
            for x in range(7):
                services.pop()
            
            for service in services:
                serviceObj = service.split(None, 4)
                service = {
                    "id": len(serviceList) + 1,
                    "unit": serviceObj[0],
                    "load": serviceObj[1],
                    "active": serviceObj[2],
                    "sub": serviceObj[3],
                    "description": serviceObj[4],
                    }
                serviceList.append(service)
            return serviceList
        else:
            print(f"Error getting systemd service names: {error}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




