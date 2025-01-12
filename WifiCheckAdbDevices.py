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


def get_info_device_ipv4(target):
    adb_s = f"{adb_path} -s {target} "
    serial_number_cmd = adb_s + "shell getprop ro.serialno"
    model_cmd = adb_s + "shell getprop ro.product.model"
    release_cmd = adb_s + "shell getprop ro.build.version.release"
    sdk_cmd = adb_s + "shell getprop ro.build.version.sdk"
    adb_s_device_id = f"{adb_path} -s {target} "
    
    
    serial_number= subprocess.run(serial_number_cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    model = subprocess.run(model_cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    release = subprocess.run(release_cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    sdk = subprocess.run(sdk_cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    description = f"Device ID: {target}({serial_number}): Model: {model}, Release: {release}, SDK: {sdk}"
    
    return description


def get_full_description_of_devices(target):
    adb_s = f"{adb_path} -s {target} shell getprop"
    print ("\n\n\n")
    print ("TARGET: ", target)
    
    result = subprocess.run(adb_s.split(), stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    return result.stdout.decode('utf-8')

ipv4_to_one_line_description = {}
for ipv4 in array:
    ipv4_to_one_line_description [ipv4]=get_info_device_ipv4(ipv4)

for ipv4 in array:
    print(ipv4_to_one_line_description[ipv4])
    
  
ipv4_to_full_getprop= {}    
bool_use_full_description = False
if bool_use_full_description:  
    for ipv4 in array:
        ipv4_to_full_getprop[ipv4]= get_full_description_of_devices(ipv4)



def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1
    print('00:00')

countdown_timer(10)