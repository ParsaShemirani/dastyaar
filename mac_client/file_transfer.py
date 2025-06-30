import requests
import os
import time
import threading
import sys

FILE_TRANSFER_API = "http://192.168.1.4:8321"  # update as needed

def download_file(server_file_path, local_directory):
    file_name = os.path.basename(server_file_path)
    local_path = os.path.join(local_directory, file_name)

    url = f"{FILE_TRANSFER_API}/download_file"
    params = {
        'server_file_path': server_file_path
    }
    response = requests.get(url, params=params, stream=True)

    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def upload_file(local_file_path, server_directory="/home/parsa/temporary"):
    file_name = os.path.basename(local_file_path)
    file_size = os.path.getsize(local_file_path)
    chunk_size = 10 * 1024 * 1024

    stop_flag = threading.Event()
    def show_progress():
        while not stop_flag.is_set():
            status_resp = requests.get(f"{FILE_TRANSFER_API}/upload_status", params={"filename": file_name})
            last_offset_hex = status_resp.json().get("last_offset")
            uploaded = int(last_offset_hex, 16) if last_offset_hex else 0
            percent = min(100, uploaded * 100 // file_size)
            sys.stdout.write(f"\rUploading: {percent}% [{uploaded}/{file_size} bytes]")
            sys.stdout.flush()
            time.sleep(5)
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.start()

    status_resp = requests.get(f"{FILE_TRANSFER_API}/upload_status", params={"filename": file_name})
    last_offset_hex = status_resp.json().get("last_offset")
    start_offset = int(last_offset_hex, 16) + chunk_size if last_offset_hex else 0

    with open(local_file_path, 'rb') as f:
        f.seek(start_offset)

        offset = start_offset
        while offset < file_size:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break

            files = {"chunk": (f"{offset:016X}", chunk_data)}
            data = {
                "filename": file_name,
                "offset": offset,
            }

            response = requests.post(f"{FILE_TRANSFER_API}/upload_chunk", files=files, data=data)
            if response.status_code != 200:
                print(f"Upload failed at offset {offset}")
                break

            offset += chunk_size
        
        response = requests.post(
            f"{FILE_TRANSFER_API}/assemble_file",
            data={
                "filename": file_name,
                "server_directory": server_directory,
                "expected_size": file_size
            }
        )

        if response.ok:
            print("\nFile assembled on server.")
        else:
            print("\nAssembly failed:", response.text)

    stop_flag.set()
    progress_thread.join()

    print("Upload completed.")



"""
from mac_client.file_transfer import upload_file as uf
uf('/Users/parsashemirani/Desktop/guzrecording.mov')

"""

"""
from mac_client.file_transfer import upload_file as uf
uf('/Users/parsashemirani/Main/Inbox/HINAEMAIL.eml', '/home/parsa/')

"""