import re
import os
from datetime import datetime, timezone
from mac_client import console

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
    thing = f"""\
from server import file_functions as ff
from server import read_filebase as rfb
basename = ff.extract_basename_from_file_path('{file_path}')
file_hash = ff.extract_hash_from_basename(basename)

print(rfb.get_version_number_via_hash(file_hash))

"""
    james = console.push_code(thing)
    print(james)
    print(type(james))
    # Make sure not duplicate:
    

"""
from mac_client.ingestor import make_pending as mp
mp('tomatoesaregood-v2-3a13fded334a292487416ec946330b36c04c7198430c0d74afa1aee66fbbd889.txt')
"""






"""
123-_567_-planmaster-v3-663c95c506b730e56b535ed1e52975b33c66012e23a978ed749072c1fd2e4c31.txt
123-_334_-planmaster-v2-e7f6e8198bc0fd3f9741f9b1c035c8719e8a01623c71c3e81237daa9ff5fe11c.txt
123-_224_-IMG_3979-v2-86af08b512a660bfe5f241fca9ac1545be11fdc7e07041d3e97379c518ce5f83.jpg
123-_990_-journalbase_recording-v1-1495d1b6ac36d1cc31d311a92b6b668362368ee7d12354a8b230146089d9266d.m4a
"""