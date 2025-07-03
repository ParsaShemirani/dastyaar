from mac_client.file_transfer import upload_file
import os
from mac_client import console

pending_directory = '/Users/parsashemirani/Main/test_folders/pending_transfer_test'
server_temp_directory='/home/parsa/transfers/completed'


def ingest_file(file_path):
    upload_file(
        local_file_path=file_path,
        server_directory=server_temp_directory
    )
    server_temp_path = os.path.join(server_temp_directory, os.path.basename(file_path))

    response = int(console.push_code(f"""\
file_path = '''{server_temp_path}'''

from server.ingest import ingest_or_update
file_dict = ingest_or_update(file_path)

# Check result
from server.read_filebase import get_file_id_via_hash
if not get_file_id_via_hash(hash=file_dict['hash']):
    print("FAIL")

print(file_dict)
"""))
    return response



def ingest_pending():


    file_paths = []
    for f in os.listdir(pending_directory):
        full_path = os.path.join(pending_directory, f)
        if os.path.isfile(full_path) and not f.startswith('.'):
            file_paths.append(full_path)

    file_paths.sort(key=lambda path: os.path.getsize(path))


    for file_path in file_paths:
        ingest_file(file_path=file_path)
        console.soft_reset()
