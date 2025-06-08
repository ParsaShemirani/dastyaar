import hashlib
import os
from datetime import datetime, timezone
import shutil
import re
from zoneinfo import ZoneInfo
# Note on LOGIC: If function provided with file path, will return value. If provided with filedict, will return updated filedict.

def assign_file_path(file_path):
    filedict = {}
    filedict["file_path"] = file_path
    return filedict


def generate_sha_hash(file_path=None, filedict=None,hex_output=True):
    if file_path is None:
        file_path = filedict['file_path']

    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    result = sha256_hash.hexdigest() if hex_output else sha256_hash.digest()

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["hash"] = result

def get_file_size(file_path=None, filedict=None):
    if file_path is None:
        file_path = filedict['file_path']

    result = os.path.getsize(file_path)

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["size"] = result

def get_file_extension(file_path=None, filedict=None):
    if file_path is None:
        file_path = filedict['file_path']

    _, ext = os.path.splitext(file_path)
    result =  ext[1:].lower() if ext else ""

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["extension"] = result

def get_created_time(file_path=None, filedict=None):
    if file_path is None:
        file_path = filedict['file_path']

    stat = os.stat(file_path)
    unix_created = stat.st_birthtime if hasattr(stat, 'st_birthtime') else os.path.getctime(file_path)
    dt_created_time = datetime.fromtimestamp(unix_created, tz=timezone.utc)
    result = dt_created_time.strftime("%Y-%m-%d %H:%M:%S")

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["ts"] = result

def get_modified_time(file_path=None, filedict=None):
    if file_path is None:
        file_path = filedict['file_path']

    stat = os.stat(file_path)
    unix_modified = stat.st_mtime
    dt_modified_time = datetime.fromtimestamp(unix_modified, tz=timezone.utc)
    result = dt_modified_time.strftime("%Y-%m-%d %H:%M:%S")

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["ts"] = result

def get_current_time():
    dt_now = datetime.now(timezone.utc)
    result = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    return result

def generate_new_file_path(file_path=None, filedict=None,new_name=None):
    if file_path is None:
        file_path = filedict['file_path']

    if new_name is None:
        new_name = filedict['name']
    directory = os.path.dirname(file_path)
    result = os.path.join(directory, new_name)

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["new_file_path"] = result

def rename_file(filedict):
    os.rename(filedict['file_path'], filedict['new_file_path'])

def copy_file(dst_dir,file_path=None, filedict=None):
    if file_path is None:
        file_path = filedict['file_path']

    filename = os.path.basename(file_path)
    dst_path = os.path.join(dst_dir, filename)
    shutil.copy2(file_path, dst_path)

def generate_new_filename(filedict):
    file_path = filedict['file_path']
    pattern = r'^(.+)-v(\d+)-([0-9A-Fa-f]+)(\.[^.]+)$'
    filename = os.path.basename(file_path)
    m = re.match(pattern, filename)
    basename = m.groups(1)
    ext = m.groups(4)
    new_name = f"{basename}-v{filedict['version_number']}-{filedict['new_hash']}{ext}"
    return new_name

def extract_voice_rec_ts(file_path=None, filedict=None):
    if file_path is None:
        file_path = filedict['file_path']
    
    base = os.path.splitext(os.path.basename(file_path))[0]
    dt = (
        datetime.strptime(base, "%Y%m%d-%H%M%S")
        .replace(tzinfo=ZoneInfo("America/Los_Angeles"))
        .astimezone(ZoneInfo("UTC"))
    )
    result = dt.strftime("%Y-%m-%d %H:%M:%S")

    if file_path is not None:
        return result
    elif filedict is not None:
        filedict["ts"] = result

