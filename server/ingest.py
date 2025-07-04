from server import file_functions, read_filebase, write_filebase, upsert
import os
import shutil

def ingest_or_update_file(file_path):

    file_dict = {}

    file_dict['hash'] = file_functions.generate_sha_hash(
        file_path=file_path
    )

    file_dict['size'] = file_functions.get_file_size(file_path=file_path)

    file_dict['extension'] = file_functions.get_file_extension(file_path=file_path)

    file_dict['ingested_ts'] = file_functions.get_current_time()

    file_dict['basename'] = file_functions.extract_basename_from_file_path(file_path=file_path)
    file_dict['name_hash'] = file_functions.extract_hash_from_basename(basename=file_dict['basename'])
    file_dict['rootname'] = file_functions.extract_rootname_from_basename(basename=file_dict['basename'])


    file_dict['previous_version'] = read_filebase.get_version_number_via_hash(hash=file_dict['name_hash'])
    if file_dict['hash'] == file_dict['name_hash']:
        if file_dict['previous_version']:
            file_dict['version_number'] = file_dict['previous_version']
    elif file_dict['previous_version']:
        file_dict['version_number'] = file_dict['previous_version'] + 1
    else:
        file_dict['version_number'] = 1

    
    file_dict['name'] = file_functions.generate_new_filename(
        rootname=file_dict['rootname'],
        version_number=file_dict['version_number'],
        hash=file_dict['hash'],
        extension=file_dict['extension']
    )


    all_file_dict = upsert.upsert_file(file_dict)


    if not file_dict['id']:
        file_dict['id'] = read_filebase.get_file_id_via_hash(
            hash=file_dict['hash']
        )
    
    new_file_path = file_functions.generate_new_file_path(
        file_path=file_path,
        new_name=file_dict['name']
    )
    os.rename(file_path, new_file_path)

    intake_path = read_filebase.get_location_path_via_id(
        location_id=1
    )
    intake_file_path = os.path.join(intake_path, file_dict['name'])
    shutil.move(new_file_path, intake_file_path)
    write_filebase.associate_location(
        file_id=file_dict['id'],
        location_id=1
    )

    return all_file_dict




def get_version_number_via_file_path(file_path):
    basename = file_functions.extract_basename_from_file_path('{file_path}')
    name_hash = file_functions.extract_hash_from_basename(basename)
    if name_hash:
        last_version = read_filebase.get_version_number_via_hash(name_hash)
        return last_version + 1
    else:
        return 1