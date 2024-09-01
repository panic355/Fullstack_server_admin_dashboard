# Import blueprints from each module to expose them at the package level
from .account_management import account_management_bp
from .ssh_management import ssh_management_bp
from .vm_management import vm_management_bp
from .network_management import network_management_bp
from .storage_management import storage_management_bp
from .system_management import system_management_bp

# List all blueprints to be available when modules is imported
__all__ = [
    'account_management_bp',
    'ssh_management_bp',
    'vm_management_bp',
    'network_management_bp',
    'storage_management_bp',
    'system_management_bp'
]