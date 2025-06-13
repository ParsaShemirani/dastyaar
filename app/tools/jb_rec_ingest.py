from app.tools.filedata import FileData
from app.tools import file_functions as ff
import os
from pprint import pprint

def main(file_path):
    file_object = FileData(file_path=file_path)
    file_object.filld_hash()

    if not file_object.is_unique():
        raise Exception("File already exists in filebase")
    
    file_object.filld_size()
    file_object.filld_extension()

    file_object.version_number = 1

    # Timestamps
    file_object.ts = ff.extract_voice_rec_ts(
        file_path=file_object.file_path
    )
    file_object.filld_ingested_ts()

    # Name
    file_object.rootname = "journalbase_recording"
    file_object.filld_name()
    file_object.filld_new_file_path()

    # Insert into filebase
    file_object.filld_file_dict()
    file_object.insert_file_dict()

    file_object.location_id = 1
    file_object.associate_all()


    # Rename | Copy | Remove setup
    file_object.rename_file()
    ff.scp_copy(
        local_path=file_object.new_file_path,
        remote_user='parsa',
        remote_host='192.168.1.4',
        remote_path='/mnt/wdhd'
    )
    file_object.remove_file()

    print("All attributes:")
    pprint(vars(file_object))

    

def folder_main():
    folder_path = '/Users/parsashemirani/Library/Mobile Documents/iCloud~com~dayananetworks~voicerecordpro/Documents'


    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.startswith('.') or not os.path.isfile(file_path):
            continue
        print(f"\nProcessing file: {filename}")

        main(file_path=file_path)
"""
from app.tools.jb_rec_ingest import folder_main as fm
fm()
"""