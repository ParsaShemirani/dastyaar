from mac_client.file_transfer import upload_file
import os
import re
from mac_client import console


def file_id_from_temp_name(filename):
    match = re.search(r'123-_([0-9]+)_-([^-][\w\-\.]+)', filename)
    
    if match:
        number = int(match.group(1))
        core_file_name = match.group(2)
        return number
    else:
        return None

def transferer():
    pending_directory = '/Users/parsashemirani/Main/test_folders/pending_transfer_test'
    file_paths = []
    for f in os.listdir(pending_directory):
        full_path = os.path.join(pending_directory, f)
        if os.path.isfile(full_path) and not f.startswith('.'):
            file_paths.append(full_path)

    file_paths.sort(key=lambda path: os.path.getsize(path))


    from pprint import pprint
    pprint(file_paths)
    for file_path in file_paths:
        upload_file(
            local_file_path=file_path,
            server_directory='/home/parsa/jameswebb'
        )
        file_id = file_id_from_temp_name(filename=file_path)
        if not file_id:
            print("GUZMAN CRITICAL GOOZ")
            exit()
        
        console.push_code(f"""\
from server.write_filebase import associate_location
result = associate_location(file_id={file_id}, location_id=1)
print(result)
""")    


"""
from mac_client.transfer_pending_to_intake import transferer
transferer()
"""