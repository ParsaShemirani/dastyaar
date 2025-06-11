from app.tools.filedata import FileData
from app.tools import file_functions as ff
from app.tools.audio_recording import interactive_transcribe
from pprint import pprint
import os
import subprocess



def main(file_path, groupings):
    file_object = FileData(file_path=file_path)
    file_object.filld_standard()

    if not file_object.is_unique():
        raise Exception("File already exists in filebase")
    
    # Display file_dict and open the file
    print("file_dict:")
    pprint(file_object.file_dict)
    subprocess.run(['open', file_object.file_path])

    if input("Press enter to procede, anything else otherwise.") == "":
        file_object.insert_and_filld_id()
    else:
        exit()

    
    # Description
    if input("Press enter to record description, anything else otherwise.") == "":
        file_object.description = interactive_transcribe()


    # Location
    file_object.location_id = 1

    # Groupings
    if groupings != []:
        file_object.groupings = groupings


    # Handle all
    file_object.handle_all()

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

    groupings = [1]

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.startswith('.') or not os.path.isfile(file_path):
            continue
        print(f"\n\n\n\n\n\nProcessing file: {filename}")

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
r = sqldb.execute_read
w = sqldb.execute_write

def o(james):
    for row in james:
        print("\nNEWMAN\n")
        pprint(dict(row))
"""
