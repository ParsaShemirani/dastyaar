from mac_client import ingest
import ast
import os

def ingest_one(file_path):
    print("\n\n")
    print(f"Ingesting file: {file_path}")
    file_dict_str = ingest.ingest_file(
        file_path=file_path
    )
    file_dict = ast.literal_eval(file_dict_str)

    if file_dict['version_number'] == 1:
        file_dict['ts'] = ingest.get_created_time(file_path=file_path)
        ingest.dicate_associate_fdescription(
            file_id=file_dict['_id']
        )
        print("fdescription associated")
    else:
        file_dict['ts'] = ingest.get_modified_time(file_path=file_path)
        print("Processed")

    ingest.update_file(file_dict=file_dict)

    new_file_path = os.path.join(os.path.dirname(file_path), file_dict['name'])
    os.rename(file_path, new_file_path)

