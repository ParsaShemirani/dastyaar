import hashlib
import os
from datetime import datetime, timezone
import shutil
import re
from zoneinfo import ZoneInfo


def generate_sha_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    result = sha256_hash.digest()
    return result

def get_file_size(file_path=None):
    result = os.path.getsize(file_path)
    return result

def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    result =  ext[1:].lower() if ext else ""
    return result

def get_created_time(file_path):
    stat = os.stat(file_path)
    unix_created = stat.st_birthtime if hasattr(stat, 'st_birthtime') else os.path.getctime(file_path)
    dt_created_time = datetime.fromtimestamp(unix_created, tz=timezone.utc)
    result = dt_created_time.strftime("%Y-%m-%d %H:%M:%S")
    return result

def get_modified_time(file_path):
    stat = os.stat(file_path)
    unix_modified = stat.st_mtime
    dt_modified_time = datetime.fromtimestamp(unix_modified, tz=timezone.utc)
    result = dt_modified_time.strftime("%Y-%m-%d %H:%M:%S")
    return result

def get_current_time():
    dt_now = datetime.now(timezone.utc)
    result = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    return result

def generate_new_file_path(file_path,new_name):
    directory = os.path.dirname(file_path)
    result = os.path.join(directory, new_name)
    return result

def rename_file(file_path, new_file_path):
    os.rename(file_path, new_file_path)

def copy_file(file_path,dst_dir):
    filename = os.path.basename(file_path)
    dst_path = os.path.join(dst_dir, filename)
    shutil.copy2(file_path, dst_path)


def generate_new_filename(rootname, version_number, hash, extension):
    hex_hash = hash.hex()
    result = f"{rootname}-v{version_number}-{hex_hash}.{extension}"
    return result


def extract_voice_rec_ts(file_path):    
    base = os.path.splitext(os.path.basename(file_path))[0]
    dt = (
        datetime.strptime(base, "%Y%m%d-%H%M%S")
        .replace(tzinfo=ZoneInfo("America/Los_Angeles"))
        .astimezone(ZoneInfo("UTC"))
    )
    result = dt.strftime("%Y-%m-%d %H:%M:%S")
    return result



def extract_basename_from_file_path(file_path):
    basename = os.path.basename(file_path)
    return basename


def extract_rootname_from_basename(basename):
    pattern = r'^(.*)-v\d+-[a-f0-9]{64}'

    match = re.match(pattern, basename)
    if match:
        return match.group(1)
    else:
        return basename

def extract_hash_from_basename(basename):
    pattern = r'-v\d+-([a-f0-9]{64})\.\w+$'
    match = re.search(pattern, basename)
    hex_hash = match.group(1) if match else None

    if hex_hash:
        return bytes.fromhex(hex_hash)
    return None