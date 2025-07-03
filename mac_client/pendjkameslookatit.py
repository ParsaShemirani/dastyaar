import re
import os
from datetime import datetime, timezone
from mac_client import console
import hashlib
import shutil

def generate_sha_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    result = sha256_hash.digest()
    return result

def get_created_time(file_path):
    stat = os.stat(file_path)
    unix_brith = stat.st_birthtime if hasattr(stat, 'st_birthtime') else os.path.getctime(file_path)
    unix_modified = stat.st_mtime
    unix_created = min(unix_brith, unix_modified)
    dt_created_time = datetime.fromtimestamp(unix_created, tz=timezone.utc)
    result = dt_created_time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return result

def get_modified_time(file_path):
    stat = os.stat(file_path)
    unix_modified = stat.st_mtime
    dt_modified_time = datetime.fromtimestamp(unix_modified, tz=timezone.utc)
    result = dt_modified_time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return result

def extract_file_id_and_name(filename):
    match = re.match(r'123-_([0-9]+)_-([^-][\w\-\.]+)', filename)
    
    if match:
        number = match.group(1)
        new_filename = match.group(2)
        return number, new_filename
    else:
        return None, None
    


def make_pending(file_path):
    file_hash = generate_sha_hash(file_path=file_path)

    uniqueness = console.push_code(f"""\
from server.read_filebase import get_file_id_via_hash as gfivh

result = gfivh({file_hash})
print(result)
""")
    if uniqueness != "None":
        print("File not unique")
        exit()

    version_number = int(console.push_code(f"""\
from server.file_functions import extract_basename_from_file_path as ebffp
from server.file_functions import extract_hash_from_basename as ehfb
from server.read_filebase import get_version_number_via_hash as gvnvh

basename = ebffp('{file_path}')
name_hash = ehfb(basename)
if name_hash:
    last_version = gvnvh(name_hash)
    print(last_version + 1)
else:
    print(1)
"""))
    
    if version_number == 1:
        timestamp = get_created_time(file_path=file_path)
    else:
        timestamp = get_modified_time(file_path=file_path)

    console.push_code(f"""\
from server.write_filebase import insert_file
insert_file({{"ts": '{timestamp}', "hash": {file_hash}}})

""")
    
    destination_folder = "/Users/parsashemirani/Main/test_folders/pending_transfer_test"
    final_path = os.path.join(destination_folder, os.path.basename(file_path))

    shutil.copy2(file_path, final_path)
    os.remove(file_path)



    



    

"""
from mac_client.ingestor import make_pending as mp
mp('/Users/parsashemirani/Main/Inbox/asdf-v1-d674522dbe2041b6bb5c05317ba578e02ed8a6b195568d3aed9f40295228107f.html')
"""

"""
from mac_client.ingestor import make_pending as mp
mp('/Users/parsashemirani/Main/Inbox/VID_20141228_211947.mp4')
"""





"""
123-_567_-planmaster-v3-663c95c506b730e56b535ed1e52975b33c66012e23a978ed749072c1fd2e4c31.txt
123-_334_-planmaster-v2-e7f6e8198bc0fd3f9741f9b1c035c8719e8a01623c71c3e81237daa9ff5fe11c.txt
123-_224_-IMG_3979-v2-86af08b512a660bfe5f241fca9ac1545be11fdc7e07041d3e97379c518ce5f83.jpg
123-_990_-journalbase_recording-v1-1495d1b6ac36d1cc31d311a92b6b668362368ee7d12354a8b230146089d9266d.m4a
"""


"""
from server.sqliteinterface import SQLiteInterface as SQ
db = SQ("/home/parsa/serverfiles/filebase_test.db")
r = db.execute_write("DELETE FROM files WHERE id = 209")
print(r)
"""