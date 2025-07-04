from server.read_filebase import get_all_via_id
from server.write_filebase import insert_file, update_file



def upsert_file(file_dict, overwrite=False):
    if '_id' in file_dict:
        file_id = file_dict['_id']

        filtered_dict = {k: v for k, v in file_dict.items() if not k.startswith('_')}
        if not filtered_dict:
            return
            
        current_record = get_all_via_id(file_id=file_id)
        if not current_record:
            raise ValueError(f"No record found with id: {file_id}")
            
        columns_to_update = {}
        if overwrite:
            columns_to_update = filtered_dict
        else:
            for key, value in filtered_dict.items():
                if key not in current_record or current_record[key] is None:
                    columns_to_update[key] = value
        if not columns_to_update:
            return
            
        update_file(file_id, columns_to_update)
        
    else:
        filtered_dict = {k: v for k, v in file_dict.items() if not k.startswith('_')}
        if not filtered_dict:
            return
            
        insert_file(filtered_dict)