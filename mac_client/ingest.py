from mac_client.file_transfer import upload_file
import os
from mac_client import console

server_temp_directory='/home/parsa/transfers/completed'

import os
from datetime import datetime, timezone


def ingest_file(file_path):
    upload_file(
        local_file_path=file_path,
        server_directory=server_temp_directory
    )
    server_temp_path = os.path.join(server_temp_directory, os.path.basename(file_path))

    response = console.push_code(f"""\
file_path = '''{server_temp_path}'''

from server.ingest import ingest_or_update
file_dict = ingest_or_update(file_path)

print(file_dict)
""")
    #console.soft_reset()
    return response







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




from mac_client.dictation import dictate

def dicate_associate_fdescription(file_id):
    print("Please record fdescription")
    fdescription = dictate()
    console.push_code(f"""\
from server.write_filebase import associate_fdescription as af
af(
file_id={file_id},
description='''{fdescription}'''
)
""")
    
def dicate_associate_gdescription(grouping_id):
    print("Please record gdescription")
    gdescription = dictate()
    console.push_code(f"""\
from server.write_filebase import associate_gdescription as ag
ag(
grouping_id={grouping_id},
description='''{gdescription}'''
)
""")