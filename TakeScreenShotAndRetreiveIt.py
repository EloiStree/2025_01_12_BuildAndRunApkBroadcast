import os
import subprocess
import re
import time


bool_only_by_wifi=False
bool_save_additional_with_timestamp=True

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

if bool_only_by_wifi:
    array = keep_only_ivp4_addresses(array)
print (array)

array = remove_5555_port(array)
print (array)


def print_adb_devices_id():
    print ("Connected devices:")
    result = subprocess.run([f"{adb_path}", 'devices'], stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8').strip())


string_python_file_path = os.path.abspath(__file__)
string_folder_script_root = os.path.dirname(string_python_file_path)
screenshot_folder= os.path.join(string_folder_script_root, "screenshots")

def take_adb_screentshot(target):
    adb_s = f"{adb_path} -s {target}"
    screen_shot_cmd = f"{adb_s} shell screencap -p /sdcard/screen.png"
    result = subprocess.Popen(screen_shot_cmd, shell=True)
    print("Taking screenshot for device:", target)
    
def pull_back_screentshot(path, target):
    adb_s = f"{adb_path} -s {target}"
    pull_cmd = f"{adb_s} pull /sdcard/screen.png {path}"
    print(f"Pulling screenshot for device {target}: {path}")
    result = subprocess.Popen(pull_cmd, shell=True)

def get_serial_number(device_id):
    result = subprocess.run([f"{adb_path}", '-s', device_id, 'shell', 'getprop', 'ro.serialno'], stdout=subprocess.PIPE)
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


if bool_save_additional_with_timestamp:
    def duplicate_screenshot_with_timestamp(path):
        from datetime import datetime
        import shutil
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path_with_timestamp = path.replace(".png", f"_{timestamp}.png")
        shutil.copyfile(path, path_with_timestamp)
        
    for device in array:
        serial = ipv4_to_serial[device]
        path_screen_shot_in_folder = os.path.join(screenshot_folder, serial, "ScreenShot.png")
        duplicate_screenshot_with_timestamp(path_screen_shot_in_folder)
print("Wait 4 screenshot to be copy ")
time.sleep(5)

print("Gathering all screenshots in one folder")

def copy_file_in_gather_folder(path_gather, path_file, serial):
    import shutil
    if not os.path.exists(path_gather):
        os.makedirs(path_gather)
    shutil.copyfile(path_file, os.path.join(path_gather, f"{serial}.png"))

path_gather_folder = os.path.join(string_folder_script_root, "screenshots", "gather")
for device in array:
    serial = ipv4_to_serial[device]
    path_screen_shot_in_folder = os.path.join(screenshot_folder, serial, "ScreenShot.png")
    copy_file_in_gather_folder(path_gather_folder, path_screen_shot_in_folder, serial)

print("Done ")



def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1
    print('00:00')

countdown_timer(10)