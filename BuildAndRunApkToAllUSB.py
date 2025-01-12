import os
import time


package_name = "be.elab.ntpintpigame"


print("Current script path:", os.path.abspath(__file__))
string_path_script_root = os.path.dirname(os.path.abspath(__file__))



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
    
    
def list_connected_devices():
    result = os.popen("adb devices").read()
    lines = result.strip().split('\n')
    devices = [line.split()[0] for line in lines[1:] if 'device' in line]
    return devices

connected_devices = list_connected_devices()
print("Connected devices:", connected_devices)


def install_and_launch_apk_on_device(apk_path, device_id, package_name):
    display_phone_info = f"adb -s {device_id} shell getprop ro.product.model\nadb -s {device_id} shell getprop ro.build.version.release\nadb -s {device_id} shell getprop ro.build.version.sdk\n"
    install_command = f"adb -s {device_id} install -r {apk_path}"
    play_command = f"adb -s {device_id} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
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
    

    
    
    
    
    