from app.tools.filedata import FileData
from app.tools import filebase_functions as fbf
from app.tools.audio_recording import interactive_transcribe
from pprint import pprint



def main(file_path):
    file_object = FileData(file_path=file_path)

    file_object.filld_universals()
    if not file_object.is_unique():
        raise Exception("File already exists in filebase")
    file_object.filld_ts
    file_object.filld_standard_naming()
    file_object.rename_file()

    file_dict = file_object.generate_file_dict()
    fbf.insert_file(file_dict=file_dict)
    file_object.filld_file_id()

    user_choice = input("Press enter to record description, anything else otherwise.")
    if user_choice == "":
        file_object.description = interactive_transcribe()
        fbf.associate_description(
            file_id=file_object.file_id,
            description=file_object.description
        )

    fbf.associate_location(
        file_id=file_object.file_id,
        location_id=1
    )

    #file_object.groupings = [3]
    if hasattr(file_object, 'groupings'):
        for grouping in file_object.groupings:
            fbf.associate_groupings(
                file_id=file_object.file_id,
                grouping_id=grouping
            )

    print("All attributes:")
    pprint(vars(file_object))


"""F
from app.tools.tester import main as wicked
wicked('/Users/parsashemirani/Main/Inbox/testingests/DSC00871-v2-708608ae623c4272186a20170c1bc99665b454f99d71f4ec73fe65bab38f0b84.jpg')

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
