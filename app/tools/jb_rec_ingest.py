from app.tools.filedata import FileData
from app.tools import file_functions as ff
from app.tools import filebase_functions as fbf
import os
from pprint import pprint

def main(file_path):
    file_object = FileData(file_path=file_path)

    file_object.filld_universals()
    if not file_object.is_unique():
        raise Exception("File already exists in filebase")
    
    file_object.ts = ff.extract_voice_rec_ts(
        file_path=file_object.file_path
    )
    
    file_object.version_number = 1
    file_object.rootname = "journalbase_recording"
    file_object.filld_name()
    file_object.filld_new_file_path()
    file_dict = file_object.generate_file_dict()
    fbf.insert_file(file_dict=file_dict)
    file_object.filld_file_id()

    fbf.associate_location(
        file_id=file_object.file_id,
        location_id=1
    )

    file_object.rename_file()
    ff.copy_file(
        file_path=file_object.new_file_path,
        dst_dir="/Users/parsashemirani/Main/revampbase"
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