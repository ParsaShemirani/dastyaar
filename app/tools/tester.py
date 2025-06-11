from app.tools.filedata import FileData
from app.tools import file_functions as ff
from app.tools import filebase_functions as fbf
from app.tools.audio_recording import interactive_transcribe
from pprint import pprint
import os
import subprocess



def main(file_path, groupings):
    file_object = FileData(file_path=file_path)

    file_object.filld_universals()
    if not file_object.is_unique():
        raise Exception("File already exists in filebase")
    file_object.filld_ts
    file_object.filld_standard_naming()

    file_dict = file_object.generate_file_dict()
    fbf.insert_file(file_dict=file_dict)
    file_object.filld_file_id()


    # Description
    subprocess.run(['open', file_object.file_path])
    user_choice = input("Press enter to record description, anything else otherwise.")
    if user_choice == "":
        file_object.description = interactive_transcribe()
        fbf.associate_description(
            file_id=file_object.file_id,
            description=file_object.description
        )

    # Location
    fbf.associate_location(
        file_id=file_object.file_id,
        location_id=1
    )

    # Groupings
    if groupings != []:
        file_object.groupings = groupings
        file_object.handle_groupings

    # Previous ids
    if file_object.version_number != 0:
        file_object.filld_previous_id()
        file_object.handle_previous_ids()


    # Rename | Copy | Remove setup
    file_object.rename_file()
    ff.copy_file(
        file_path=file_object.new_file_path,
        dst_dir="/Users/parsashemirani/Main/revampbase"
    )
    ff.copy_file(
        file_path=file_object.new_file_path,
        dst_dir="/Users/parsashemirani/Main/ingested"
    )
    file_object.remove_file()

    print("All attributes:")
    pprint(vars(file_object))





def folder_main():
    folder_path = "/Users/parsashemirani/Main/to_ingest"

    groupings = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.startswith('.') or not os.path.isfile(file_path):
            continue
        print(f"\nProcessing file: {filename}")

        main(
            file_path=file_path,
            groupings=groupings
        )

"""
from app.tools.tester import folder_main as fm
fm()
"""




"""F
from app.tools.tester import main as wicked
wicked('/Users/parsashemirani/Main/Inbox/testingests/DSC00870-v1-1de38affeefc4fc5db46fdd165892e57a7b0023daf36144236ca746a10af6cf6.jpg')

"""
"""
from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE
from pprint import pprint
sqldb = SQLiteInterface(FILEBASE_FILE)
read = sqldb.execute_read
write = sqldb.execute_write

def output(james):
    for row in james:
        print("\nNEWMAN\n")
        pprint(dict(row))
"""
