import subprocess
import re




def get_adb_devices_id():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').strip().split('\n')
    devices = [line.split()[0] for line in lines[1:] if 'device' in line]
    return devices

def filter_out_less_that_5_length(device_ids):
    return [device_id for device_id in device_ids if len(device_id) > 5]

def keep_only_ivp4_addresses(device_ids):
    "192.168.1.114:5555"
    return [device_id for device_id in device_ids if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', device_id)]

def remove_5555_port(device_ids):
    return [device_id.split(':')[0] for device_id in device_ids]
    
array = get_adb_devices_id()
print (array)
array = keep_only_ivp4_addresses(array)
print (array)

array = remove_5555_port(array)
print (array)


def print_adb_devices_id():
    print ("Connected devices:")
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8').strip())

def close_all_connections(array):
    if not array:
        print("No devices to disconnect.")
        return
    target = array[0]
    adb_s = f"adb -s {target} "
    disconnect_cmd = adb_s + "disconnect"
    print(subprocess.run(disconnect_cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip())
    
    

print_adb_devices_id()
close_all_connections(array)
print_adb_devices_id()    


