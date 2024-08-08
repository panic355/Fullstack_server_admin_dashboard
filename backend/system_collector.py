import subprocess
import json

def get_bios_version():
    try:
        result = subprocess.run(['dmidecode', '-t', 'bios'], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.split('\n'):
            if 'Version:' in line:
                return line.split('Version:')[1].strip()
    except Exception as e:
        return str(e)

def get_cpu_info():
    try:
        result = subprocess.run(['lscpu'], stdout=subprocess.PIPE, text=True)
        cpu_info = {}
        for line in result.stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':')
                cpu_info[key.strip()] = value.strip()
        return cpu_info
    except Exception as e:
        return str(e)

def get_ram_info():
    try:
        result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE, text=True)
        ram_info = {}
        for line in result.stdout.split('\n'):
            if 'Mem:' in line:
                _, total, used, free, *_ = line.split()
                ram_info['Total'] = total
                ram_info['Used'] = used
                ram_info['Free'] = free
        return ram_info
    except Exception as e:
        return str(e)

def get_storage_devices():
    try:
        result = subprocess.run(['lsblk', '-o', 'NAME,SIZE,TYPE'], stdout=subprocess.PIPE, text=True)
        storage_devices = []
        for line in result.stdout.split('\n'):
            if 'disk' in line:
                name, size, _type = line.split()
                storage_devices.append({'Name': name, 'Size': size})
        return storage_devices
    except Exception as e:
        return str(e)

def returnSystemInfo():
    system_info = {
        'BIOS Version': get_bios_version(),
        'CPU Info': get_cpu_info(),
        'RAM Info': get_ram_info(),
        'Storage Devices': get_storage_devices()
    }

    return system_info

