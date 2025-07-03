import re
import os
from datetime import datetime, timezone
from mac_client import console
import hashlib
import shutil
from mac_client.dictation import dictate


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
    


def ingest(file_path, collection_id):
    file_dict = {}

    file_dict['hash'] = generate_sha_hash(file_path=file_path)

    uniqueness = console.push_code(f"""\
from server.read_filebase import get_file_id_via_hash as gfivh

result = gfivh({file_dict['hash']})
print(result)
""")
    if uniqueness != "None":
        print(f"File not unique: {file_path}")
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
        file_dict['ts'] = get_created_time(file_path=file_path)
    else:
        file_dict['ts'] = get_modified_time(file_path=file_path)


    console.push_code(f"""\
from server.write_filebase import insert_file
insert_file({file_dict})


from server.read_filebase import get_file_id_via_hash as gfivh
file_id = gfivh({file_dict['hash']})


from server.write_filebase import associate_grouping
associate_grouping(
file_id=file_id,
grouping_id={collection_id}
)

print(basename)
""")


    destination_folder = "/Users/parsashemirani/Main/test_folders/pending_transfer_test"
    final_path = os.path.join(destination_folder, os.path.basename(file_path))

    shutil.copy2(file_path, final_path)
    os.remove(file_path)









def make_collection_plus_pending(collection_path):
    collection_name = os.path.basename(collection_path)
    print("collection_name: ", collection_name)
    print("Dictate collection_description:\n")
    collection_description = dictate()
    collection_id = console.push_code(f"""\
from server.write_filebase import create_grouping
create_grouping(
name='{collection_name}',
_type_='collection'
)

from server.read_filebase import get_last_grouping_id as glgi
collection_id = glgi()

from server.write_filebase import associate_gdescription as agd
agd(
grouping_id = collection_id,
description = '''{collection_description}'''
)



""")
    

    for filename in os.listdir(collection_path):
        file_path = os.path.join(collection_path, filename)
        if filename.startswith('.') or not os.path.isfile(file_path):
            continue
        print(f"\nProcessing file: {filename}")
        ingest(
            file_path=file_path,
            collection_id=collection_id
        )
        console.soft_reset()





    
"""
from mac_client.collection_ingestor import ingest
ingest('/Users/parsashemirani/Main/Inbox/jamescollection/DSC00716.JPG', 18)
"""


"""
from mac_client.collection_ingestor import make_collection_plus_pending as mcpp
mcpp('/Users/parsashemirani/Main/Inbox/buzman')
"""



"""
from server.sqliteinterface import SQLiteInterface as SQ
db = SQ("/home/parsa/serverfiles/filebase_test.db")
r = db.execute_write("DELETE FROM files WHERE id = 209")
print(r)
"""





"""
db.execute_read("SELECT * FROM groupings ORDER BY id DESC LIMIT 1")
"""

"""
from server.sqliteinterface import SQLiteInterface as SQ
db = SQ("/home/parsa/serverfiles/filebase_test.db")
db.execute_write("DELETE FROM groupings WHERE id = 18")
"""