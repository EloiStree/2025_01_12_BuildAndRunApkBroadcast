import os
import subprocess
import re
import time




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


string_python_file_path = os.path.abspath(__file__)
string_folder_script_root = os.path.dirname(string_python_file_path)
screenshot_folder= os.path.join(string_folder_script_root, "screenshots")

def take_adb_screentshot(target):
    adb_s = f"adb -s {target}"
    screen_shot_cmd = f"{adb_s} shell screencap -p /sdcard/screen.png"
    result = subprocess.Popen(screen_shot_cmd, shell=True)
    print("Taking screenshot for device:", target)
    
def pull_back_screentshot(path, target):
    adb_s = f"adb -s {target}"
    pull_cmd = f"{adb_s} pull /sdcard/screen.png {path}"
    print(f"Pulling screenshot for device {target}: {path}")
    result = subprocess.Popen(pull_cmd, shell=True)

def get_serial_number(device_id):
    result = subprocess.run(['adb', '-s', device_id, 'shell', 'getprop', 'ro.serialno'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

ipv4_to_serial = {}
for device in array:
    serial = get_serial_number(device)
    ipv4_to_serial[device] = serial
    print (f"Device:{device} Serial:{serial}")

for device in array:
    serial = ipv4_to_serial[device]
    take_adb_screentshot(device)
    
print("Wait 4 screenshot to be taken ")
time.sleep(5)
for device in array:
    serial = ipv4_to_serial[device]
    path_screen_shot_in_folder = os.path.join(screenshot_folder, serial, "ScreenShot.png")
    if not os.path.exists(os.path.dirname(path_screen_shot_in_folder)):
        os.makedirs(os.path.dirname(path_screen_shot_in_folder))
    pull_back_screentshot(path_screen_shot_in_folder,device)
print("Done ?")