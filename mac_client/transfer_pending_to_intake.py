from mac_client.file_transfer import upload_file
import os
from mac_client import console


def transferer():
    pending_directory = '/Users/parsashemirani/Main/test_folders/pending_transfer_test'

    server_temp_directory='/home/parsa/transfers/completed'

    file_paths = []
    for f in os.listdir(pending_directory):
        full_path = os.path.join(pending_directory, f)
        if os.path.isfile(full_path) and not f.startswith('.'):
            file_paths.append(full_path)

    file_paths.sort(key=lambda path: os.path.getsize(path))


    for file_path in file_paths:
        upload_file(
            local_file_path=file_path,
            server_directory=server_temp_directory
        )

        server_temp_path = os.path.join(server_temp_directory, os.path.basename(file_path))

        print("ABOUT TO INGEST")
        import time
        time.sleep(3)

        console.push_code(f"""\
file_path = '''{tempopath}'''


from server.file_functions import generate_sha_hash as gsh
file_hash = gsh(file_path)


from server.read_filebase import get_file_id_via_hash as gfivh
file_id = gfivh(file_hash)


file_dict = {{}}


from server.file_functions import get_file_size as gfs
file_dict['size'] = gfs(file_path)


from server.file_functions import get_file_extension as gfe
file_dict['extension'] = gfe(file_path)

from server.file_functions import get_current_time as gct
file_dict['ingested_ts'] = gct()





from server.file_functions import extract_basename_from_file_path as ebffp
basename = ebffp(file_path)


from server.file_functions import extract_rootname_from_basename as erfb
rootname = erfb(basename)

from server.file_functions import extract_hash_from_basename as ehfb
name_hash = ehfb(basename)


from server.read_filebase import get_version_number_via_hash as gvnvh
previous_version = gvnvh(name_hash)
if previous_version:
    file_dict['version_number'] = previous_version + 1
else:
    file_dict['version_number'] = 1

from server.file_functions import generate_new_filename as gnf
file_dict['name'] = gnf(
rootname=rootname,
version_number=file_dict['version_number'],
hash=file_hash,
extension=file_dict['extension']
)


from server.file_functions import generate_new_file_path as gnfp
new_path = gnfp(
file_path=file_path,
new_name=file_dict['name']
)

from server.write_filebase import update_file
update_file(
file_id=file_id,
file_dict=file_dict
)






# Now moving to intake drive

import os
os.rename(file_path, new_path)


from server.file_functions import copy_file
copy_file(
file_path=new_path,
dst_dir='/mnt/wdhd/test_base'
)

os.remove(new_path)

from server.write_filebase import associate_location
result = associate_location(file_id=file_id, location_id=1)


""")    
        #console.soft_reset()



"""
from mac_client.transfer_pending_to_intake import transferer
transferer()
"""