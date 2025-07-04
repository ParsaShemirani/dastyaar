from server.read_filebase import get_all_via_file_id, get_file_id_via_hash
from server.write_filebase import insert_file, update_file, associate_fdescription, associate_grouping, associate_location



def upsert_file(file_dict, overwrite=False):
    # Files table processing
    files_columns = {'name', 'ts', 'ingested_ts', 'version_number', 'extension', 'size', 'hash'}
    filtered_dict = {k: v for k, v in file_dict.items() if k in files_columns}

    if filtered_dict:
        if 'id' in file_dict:
            file_id = file_dict['id']
                
            current_record = get_all_via_file_id(file_id=file_id)
            if not current_record:
                raise ValueError(f"No record found with id: {file_id}")
                
            columns_to_update = {}
            if overwrite:
                columns_to_update = filtered_dict
            else:
                for key, value in filtered_dict.items():
                    if key not in current_record or current_record[key] is None:
                        columns_to_update[key] = value

            if columns_to_update:
                update_file(file_id, columns_to_update)
            
        else:   
            if 'hash' not in file_dict:
                raise ValueError("Hash is required for new file insertion")
            insert_file(filtered_dict)
            file_id = get_file_id_via_hash(hash=file_dict['hash'])

    current_record = get_all_via_file_id(file_id=file_id)

    # Associating
    if 'groupings' in file_dict and file_dict['groupings'] is not None:
        grouping_ids = [g['id'] for g in file_dict['groupings']]
        current_grouping_ids = [g['id'] for g in current_record['groupings']]
        new_groupings = [gid for gid in grouping_ids if gid not in current_grouping_ids]
        for gid in new_groupings:
            associate_grouping(file_id=file_id, grouping_id=gid)
        
    if 'locations' in file_dict and file_dict['locations'] is not None:
        location_ids = [l['id'] for l in file_dict['locations']]
        current_location_ids = [l['id'] for l in current_record['locations']]
        new_locations = [lid for lid in location_ids if lid not in current_location_ids]
        for lid in new_locations:
            associate_location(file_id=file_id, location_id=lid)

    if 'fdescription' in file_dict and file_dict['fdescription'] is not None:
        associate_fdescription(file_id=file_id, description=file_dict['fdescription'])
