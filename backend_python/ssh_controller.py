import paramiko

class SSHClient:
    def __init__(self):
        self.ssh_client = None

    def connect(self, host, username, password):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=host, username=username, password=password)
            return True, None
        except Exception as e:
            return False, str(e)

    def execute_command(self, command):
        if self.ssh_client is None:
            return 'Not connected to any SSH session.'

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            output = stdout.read().decode() + stderr.read().decode()
            return output
        except Exception as e:
            return str(e)

    def close_connection(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None