import subprocess

def check_sudo_password(password):
    """
    Check if the provided password can be used for sudo access.
    
    :param password: The password to check.
    :return: True if the password is correct, False otherwise.
    """
    try:
        # Test the password by running a harmless command with sudo
        result = subprocess.run(
            ['sudo', '-S', 'true'],
            input=password + '\n',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # If return code is 0, the password is correct
        return result.returncode == 0
    except Exception as e:
        # Handle exceptions or log them as needed
        return False