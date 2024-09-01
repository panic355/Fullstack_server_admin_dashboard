from flask import Flask
from modules.account_management import account_management_bp
from modules.ssh_management import ssh_management_bp
from modules.vm_management import vm_management_bp
from modules.network_management import network_management_bp
from modules.storage_management import storage_management_bp
from modules.system_management import system_management_bp
from modules.log_management import log_management_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints for different modules
    app.register_blueprint(account_management_bp)
    app.register_blueprint(ssh_management_bp)
    app.register_blueprint(vm_management_bp)
    app.register_blueprint(network_management_bp)
    app.register_blueprint(storage_management_bp)
    app.register_blueprint(system_management_bp)
    app.register_blueprint(log_management_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)