from server import file_functions, read_filebase, write_filebase
import os
import shutil

def ingest_or_update(file_path):

    file_dict = {}

    file_dict['hash'] = file_functions.generate_sha_hash(
        file_path=file_path
    )

    file_dict['size'] = file_functions.get_file_size(file_path=file_path)

    file_dict['extension'] = file_functions.get_file_extension(file_path=file_path)

    file_dict['ingested_ts'] = file_functions.get_current_time()

    file_dict['_basename'] = file_functions.extract_basename_from_file_path(file_path=file_path)
    file_dict['_name_hash'] = file_functions.extract_hash_from_basename(basename=file_dict['_basename'])
    file_dict['_rootname'] = file_functions.extract_rootname_from_basename(basename=file_dict['_basename'])

    file_dict['_previous_version'] = read_filebase.get_version_number_via_hash(hash=file_dict['_name_hash'])
    if file_dict['_previous_version']:
        file_dict['version_number'] = file_dict['_previous_version'] + 1
    else:
        file_dict['version_number'] = 1
    
    file_dict['name'] = file_functions.generate_new_filename(
        rootname=file_dict['_rootname'],
        version_number=file_dict['version_number'],
        hash=file_dict['hash'],
        extension=file_dict['extension']
    )

    file_dict['_id'] = read_filebase.get_file_id_via_hash(hash=file_dict['hash'])

    if file_dict['_id']:
        file_dict['_ingest_or_update'] = 'update'
        write_filebase.update_file(
            file_id=file_dict['_id'],
            file_dict=file_dict
        )
    else:
        file_dict['_ingest_or_update'] = 'ingest'
        write_filebase.insert_file(
            file_dict=file_dict
        )
        file_dict['_id']= read_filebase.get_file_id_via_hash(
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
        file_id=file_dict['_id'],
        location_id=1
    )

    return file_dict
