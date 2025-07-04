import os
import hashlib
import shutil
from datetime import datetime, timezone
from mac_client.file_transfer import upload_file
from mac_client import console
from mac_client.dictation import dictate



PENDING_UPLOAD_FOLDER = '/Users/parsashemirani/main/pending_upload'



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


def make_pending(file_path, file_dict={}):
    file_dict['hash'] = generate_sha_hash(file_path=file_path)
    uniqueness = console.push_code(f"""\
from server.read_filebase import get_file_id_via_hash

result = get_file_id_via_hash({file_dict['hash']})
print(result)
""")
    if uniqueness != "None":
        raise ValueError("File not unique")

    if not file_dict.get('ts'):
        file_dict['version_number'] = int(console.push_code(f"""\
from server.ingest import get_version_number_via_file_path
print(get_version_number_via_file_path(file_path='''{file_path}'''))
    """))
        if file_dict['version_number'] == 1:
            file_dict['ts'] = get_created_time(file_path=file_path)
        else:
            file_dict['ts'] = get_modified_time(file_path=file_path)

    console.push_code(f"""\
from server.upsert import upsert_file
upsert_file(file_dict={file_dict})
""")
    
    shutil.copy2(file_path, os.path.join(
        PENDING_UPLOAD_FOLDER,
        os.path.basename(file_path)
    ))


def upload_and_ingest_pending_file(file_name):
    upload_file(
        local_file_path=os.path.join(PENDING_UPLOAD_FOLDER, file_name)
    )

    all_file_dict = console.push_code(f"""\
import os
uploaded_dir = '/home/parsa/uploads/uploaded'
from server.ingest import ingest_or_update_file
file_path=os.path.join(uploaded_dir, '''{file_name}''')
all_file_dict = ingest_or_update_file(file_path=file_path)

os.remove(os.path.join(uploaded_dir, all_file_dict['name']))

print(all_file_dict)

""")
    #console.soft_reset()
    return all_file_dict













