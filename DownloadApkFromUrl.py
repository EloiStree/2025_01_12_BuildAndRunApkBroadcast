import os
import sys
import requests

# pip install gdown
import gdown


path_file_containing_download_link = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download_apk_link.txt")

def download_apk(url, save_path):
    if "drive.google.com" in url:
        file_id = url.split('/')[-2]
        print (f"File ID: {file_id}")
        url = f"https://drive.google.com/uc?id={file_id}"
        print ("Downloading from Google Drive")
        gdown.download(url, save_path, quiet=False)
        print(f"APK downloaded successfully and saved to {save_path}")
    else :
        print ("Downloading from URL")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"APK downloaded successfully and saved to {save_path}")
        else:
            print(f"Failed to download APK. Status code: {response.status_code}")

def main():
    
    default_url = "https://example.com/path/to/default.apk"
    if not os.path.exists(path_file_containing_download_link):
        with open(path_file_containing_download_link, "w") as f:
            f.write(default_url)
    with open(path_file_containing_download_link) as f:
        url = f.read().strip()
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(script_dir, "build")
    os.makedirs(build_dir, exist_ok=True)  
    save_path = os.path.join(build_dir, "last_build.apk")
    download_apk(url, save_path)
    

if __name__ == "__main__":
    main()