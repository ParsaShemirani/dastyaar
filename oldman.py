# Will git update it?

import requests
import os
from app.tools.settings import FILE_TRANSFER_API


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

def upload_file(local_file_path, server_directory):
    file_name = os.path.basename(local_file_path)

    url = f"{FILE_TRANSFER_API}/upload_file"
    with open(local_file_path, 'rb') as f:
        files = {
            "file": (file_name, f)
        }
        data = {
            "server_directory": server_directory
        }
        response = requests.post(url=url, files=files, data=data)



