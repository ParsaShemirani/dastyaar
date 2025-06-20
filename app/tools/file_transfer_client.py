import requests
import os
from app.tools.settings import FILE_TRANSFER_API
import time

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
    file_size = os.path.getsize(local_file_path)
    chunk_size = 10 * 1024 * 1024
    total_chunks = (file_size + chunk_size - 1) // chunk_size
    
    url = f"{FILE_TRANSFER_API}/upload_chunk"
    
    with open(local_file_path, 'rb') as f:
        for chunk_number in range(total_chunks):
            chunk_data = f.read(chunk_size)
            
            files = {"chunk": (f"chunk_{chunk_number}", chunk_data)}
            data = {
                "filename": file_name,
                "chunk_number": chunk_number,
                "total_chunks": total_chunks,
                "server_directory": server_directory
            }
            
            requests.post(url=url, files=files, data=data)







def upload_file_timed(local_file_path, server_directory):
    file_name = os.path.basename(local_file_path)
    file_size = os.path.getsize(local_file_path)
    chunk_size = 10 * 1024 * 1024
    total_chunks = (file_size + chunk_size - 1) // chunk_size
    
    url = f"{FILE_TRANSFER_API}/upload_chunk"
    
    bytes_uploaded = 0
    start_time = time.time()
    last_update_time = start_time

    with open(local_file_path, 'rb') as f:
        for chunk_number in range(total_chunks):
            chunk_data = f.read(chunk_size)
            chunk_len = len(chunk_data)
            
            files = {"chunk": (f"chunk_{chunk_number}", chunk_data)}
            data = {
                "filename": file_name,
                "chunk_number": chunk_number,
                "total_chunks": total_chunks,
                "server_directory": server_directory
            }
            
            requests.post(url=url, files=files, data=data)
            
            bytes_uploaded += chunk_len
            current_time = time.time()
            
            # Print update every 10 seconds
            if current_time - last_update_time >= 10 or chunk_number == total_chunks - 1:
                elapsed = int(current_time - start_time)
                print(f"Elapsed: {elapsed} seconds, Uploaded: {bytes_uploaded} bytes")
                last_update_time = current_time
