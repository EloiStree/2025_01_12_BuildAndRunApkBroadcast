import subprocess
import re

import os
import time
# THIS CODE WORK IN SCRPY
# use f"{adb_path}
python_path = os.path.abspath(__file__)
adb_path = os.path.join(os.path.dirname(python_path), "../adb.exe")
adb_path = os.path.abspath(adb_path)
print("ADB: ",adb_path)


def get_adb_devices_id():
    result = subprocess.run([f"{adb_path}", 'devices'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    device_ids = re.findall(r'(\w+)\s+device', output)
    return device_ids


def filter_out_less_that_5_length(device_ids):
    return [device_id for device_id in device_ids if len(device_id) > 5]


array = get_adb_devices_id()
array = filter_out_less_that_5_length(array)

def get_ivp4_of_devices(string_device_id_adb):
    result = subprocess.run([f"{adb_path}", '-s', string_device_id_adb, 'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    ip = re.findall(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
    return ip[0]


print (array)

ids_to_ipv4 = {}

for a in array:
    print(f"{a}:{get_ivp4_of_devices(a)}")
    ids_to_ipv4[a] = get_ivp4_of_devices(a)
    
for a in array:
    subprocess.run([f"{adb_path}", '-s', a, 'tcpip', '5555'], stdout=subprocess.PIPE)
    subprocess.run([f"{adb_path}", 'connect', ids_to_ipv4[a]], stdout=subprocess.PIPE)
    
print("Done")

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1
    print('00:00')

countdown_timer(10)