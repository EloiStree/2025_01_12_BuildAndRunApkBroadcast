import os
import time


# replace by the path on your computer
aapt_path = "C:\\Users\\elab\\AppData\\Local\\Android\\Sdk\\build-tools\\30.0.2\\aapt.exe"



# THIS CODE WORK IN SCRPY
python_path = os.path.abspath(__file__)
adb_path = os.path.join(os.path.dirname(python_path), "../adb.exe")
adb_path = os.path.abspath(adb_path)
print("ADB: ",adb_path)



package_name = "be.elab.ntpintpigame"


string_python_script_path = os.path.abspath(__file__)
string_folder_script_root = os.path.dirname(string_python_script_path)
print("Current script path:", string_python_script_path)
string_path_script_root = string_folder_script_root

string_build_folder= os.path.join(string_path_script_root, "build")
print("Build folder path:", string_build_folder)
if not os.path.exists(string_build_folder):
    os.makedirs(string_build_folder)


def find_apks_in_build_folder(build_folder_path):
    apk_files = []
    for root, dirs, files in os.walk(build_folder_path):
        for file in files:
            if file.endswith(".apk"):
                apk_files.append(os.path.join(root, file))
    return apk_files

apk_files = find_apks_in_build_folder(string_path_script_root)
string_path_of_apk = apk_files[0]
for apk in apk_files:
    string_path_of_apk=apk
    print(apk)


if os.path.exists(aapt_path):
    package_name_previous=package_name
    package_name=""
    command = f"{aapt_path} dump badging {string_path_of_apk} | findstr package"
    result = os.popen(command).read()
    if result:
        package_name = result.split("name='")[1].split("'")[0]
        print("Package name found:", package_name)
    

    
def list_connected_devices():
    result = os.popen(f"{adb_path} devices").read()
    lines = result.strip().split('\n')
    devices = [line.split()[0] for line in lines[1:] if 'device' in line]
    return devices

connected_devices = list_connected_devices()
print("Connected devices:", connected_devices)


def install_and_launch_apk_on_device(apk_path, device_id, package_name):
    display_phone_info = f"{adb_path} -s {device_id} shell getprop ro.product.model\n{adb_path} -s {device_id} shell getprop ro.build.version.release\n{adb_path}  -s {device_id} shell getprop ro.build.version.sdk\n"
    install_command = f"{adb_path} -s {device_id} install -r {apk_path}"
    play_command = f"{adb_path} -s {device_id} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
    return f"{display_phone_info}\n\n{install_command}\n\n{play_command}\n\n"

string_clipboard_commands= ""
for device in connected_devices:
    string_clipboard_commands+=install_and_launch_apk_on_device(string_path_of_apk, device, package_name)

print(string_clipboard_commands)
for line in string_clipboard_commands.split('\n'):
    if line.strip() != "":
        print(line)
        os.system(line)
        time.sleep(1)
    

    
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        seconds -= 1
    print('00:00')

countdown_timer(10)
    
    
    