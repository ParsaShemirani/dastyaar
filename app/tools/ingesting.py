from app.tools.filedata import FileData
from app.tools.filebase_functions import insert_file
from app.tools.audio_recording import interactive_transcribe
import pprint
def ingest_standard(file_path):
    file_object = FileData(file_path=file_path)

    file_object.filld_hash() 
    if file_object.is_unique() == False:
        print("File already exists in database")
        exit()

    file_object.filld_version_number()
    file_object.filld_size()
    file_object.filld_extension()
    file_object.filld_ts()
    file_object.filld_name()
    file_object.description = interactive_transcribe()
    pprint.pprint(vars(file_object))
    print("NOW TIME FOR TIMID")

    file_object.mastername = 'hello man'
    file_object.timidman = 1234123
    print(file_object.mastername)

    file_dict = file_object.generate_file_dict()
    pprint.pprint(file_dict)

    insert_file(file_dict=file_dict)


"""
from app.tools.ingesting import ingest_standard
ingest_standard('/Users/parsashemirani/Main/sonysdbefubuntu/101MSDCF/DSC00919.JPG')
"""

"""
from app.tools.sqliteinterface import SQLiteInterface
sqldb = SQLiteInterface('/Users/parsashemirani/Main/dastyaar/app/tools/filebase_test.db')

"""