import os
from mac_client import ingest
from mac_client.dictation import dictate

def ingest_one(file_path):
    print("\n\n", f"Ingesting file: {file_path}")

    file_dict = {}
    choice = input("\n\n Dictate fdescription? (y for yes): ")
    if choice == "y":
        file_dict['fdescription'] = dictate()
    
    ingest.make_pending(
        file_path=file_path,
        file_dict=file_dict
    )

    all_file_dict = ingest.upload_and_ingest_pending_file(
        file_name=os.path.basename(file_path)
    )

    new_file_path = os.path.join(os.path.dirname(file_path), all_file_dict['name'])
    os.rename(file_path, new_file_path)