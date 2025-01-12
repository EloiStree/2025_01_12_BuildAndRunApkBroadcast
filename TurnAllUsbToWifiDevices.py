import subprocess
import re




def get_adb_devices_id():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    device_ids = re.findall(r'(\w+)\s+device', output)
    return device_ids


def filter_out_less_that_5_length(device_ids):
    return [device_id for device_id in device_ids if len(device_id) > 5]


array = get_adb_devices_id()
array = filter_out_less_that_5_length(array)

def get_ivp4_of_devices(string_device_id_adb):
    result = subprocess.run(['adb', '-s', string_device_id_adb, 'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    ip = re.findall(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
    return ip[0]


print (array)

ids_to_ipv4 = {}

for a in array:
    print(f"{a}:{get_ivp4_of_devices(a)}")
    ids_to_ipv4[a] = get_ivp4_of_devices(a)
    
for a in array:
    subprocess.run(['adb', '-s', a, 'tcpip', '5555'], stdout=subprocess.PIPE)
    subprocess.run(['adb', 'connect', ids_to_ipv4[a]], stdout=subprocess.PIPE)
    
print("Done")

