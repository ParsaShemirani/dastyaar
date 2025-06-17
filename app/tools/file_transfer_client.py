import requests
import os
from app.tools.settings import INTAKE_DRIVE_PATH

def download_file(file_name, local_directory, location_path=INTAKE_DRIVE_PATH):
    local_path = os.path.join(local_directory, file_name)

    url = "http://192.168.1.4:5034/download_file"
    params = {
        'file_name': file_name,
        'location_path': location_path
    }
    response = requests.get(url, params=params, stream=True)

    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def upload_file(file_path, location_path = INTAKE_DRIVE_PATH):
    file_name = os.path.basename(file_path)

    url = "http://192.168.1.4:5034/upload_file"
    with open(file_path, 'rb') as f:
        files = {
            "file": (file_name, f)
        }
        data = {
            "location_path": location_path
        }
        response = requests.post(url=url, files=files, data=data)



