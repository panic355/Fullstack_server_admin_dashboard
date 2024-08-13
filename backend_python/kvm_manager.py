import libvirt
import sys

def connect_to_libvirt():
    try:
        conn = libvirt.open('qemu:///system')
        return conn
    except libvirt.libvirtError as e:
        sys.stderr.write(f"Failed to open connection to qemu:///system: {e}")
        sys.exit(1)

def list_vms():
    conn = connect_to_libvirt()
    domains = conn.listAllDomains()
    vms = []
    for domain in domains:
        vms.append({
            'id': domain.ID(),
            'name': domain.name(),
            'state': domain.state(0)[0]
        })
    conn.close()
    return vms

def start_vm(vm_name):
    conn = connect_to_libvirt()
    try:
        domain = conn.lookupByName(vm_name)
        if domain.isActive():
            return {'status': 'VM is already running'}, 400
        domain.create()
        conn.close()
        return {'status': 'VM started successfully'}, 200
    except libvirt.libvirtError as e:
        return {'error': str(e)}, 500

def stop_vm(vm_name):
    conn = connect_to_libvirt()
    try:
        domain = conn.lookupByName(vm_name)
        if not domain.isActive():
            return {'status': 'VM is already stopped'}, 400
        domain.shutdown()
        conn.close()
        return {'status': 'VM stopped successfully'}, 200
    except libvirt.libvirtError as e:
        return {'error': str(e)}, 500

def destroy_vm(vm_name):
    conn = connect_to_libvirt()
    try:
        domain = conn.lookupByName(vm_name)
        domain.destroy()
        conn.close()
        return {'status': 'VM destroyed successfully'}, 200
    except libvirt.libvirtError as e:
        return {'error': str(e)}, 500

def delete_vm(vm_name):
    conn = connect_to_libvirt()
    try:
        domain = conn.lookupByName(vm_name)
        domain.undefine()
        conn.close()
        return {'status': f'VM {vm_name} deleted successfully'}, 200
    except libvirt.libvirtError as e:
        return {'error': str(e)}, 500