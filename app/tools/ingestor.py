from app.tools.filedata import FileData
from app.tools import file_functions as ff
from app.tools.audio_recording import interactive_transcribe
from pprint import pprint
import os
import subprocess
import time
from app.tools.settings import TO_INGEST_PATH, INGESTED_PATH, INTAKE_DRIVE_PATH
from app.tools.file_transfer_client import upload_file

def main(file_path, groupings, interactive=True):
    file_object = FileData(file_path=file_path)
    file_object.filld_standard()

    if not file_object.is_unique():
        raise Exception("File already exists in filebase")
    
    # Display file_dict and open the file
    print("file_dict:")
    pprint(file_object.file_dict)
    if interactive is True:
        if file_object.extension in ('jpg', 'mp4', 'png', 'txt', 'mov', 'm4a', 'mp3', 'avi'):
            subprocess.run(['open', file_object.file_path])

        if input("Press enter to procede, anything else otherwise.") == "":
            file_object.insert_file_dict()
        else:
            exit()
        if input("Press enter to record description, anything else otherwise.") == "":
            file_object.description = interactive_transcribe()
    else:
        file_object.insert_file_dict()
    


    # Location
    file_object.location_id = 1

    # Groupings
    if groupings != []:
        file_object.groupings = groupings


    # Associate all
    file_object.associate_all()

    # Rename | Copy | Remove setup
    file_object.rename_file()

    print("HTTP Copying file")
    upload_file(
        local_file_path=file_object.new_file_path,
        server_directory=INTAKE_DRIVE_PATH
    )
    print("HTTP copy done")
    ff.copy_file(
        file_path=file_object.new_file_path,
        dst_dir=INGESTED_PATH
    )
    file_object.remove_file()

    print("All attributes:")
    pprint(vars(file_object))





def folder_main():
    folder_path = TO_INGEST_PATH
    groupings = []
    interactive = True
    for i in range(3):
        print("CHECK GROUPINGS\n")
        print(groupings)

        time.sleep(1)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.startswith('.') or not os.path.isfile(file_path):
            continue
        print(f"\n\n\n\n\n\nProcessing file: {filename}")

        main(
            file_path=file_path,
            groupings=groupings,
            interactive=interactive
        )

"""
from app.tools.ingestor import folder_main as fm
fm()
"""

