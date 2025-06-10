from app.tools.filedata import FileData
from app.tools import filebase_functions as fbf
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


    masterman = fbf.get_file_id_via_hash(hash=file_dict['hash'])

    print("MASETERS")
    print(masterman)
    fbf.insert_file(file_dict=file_dict)


"""
from app.tools.ingesting import ingest_standard
ingest_standard('/Users/parsashemirani/Main/Inbox/DSC00919-v1-676a8b02fcc5a7012551da8a084fae35e6a273b55594c5d72053f7adf25c88c7.JPG')
"""

"""
from app.tools.sqliteinterface import SQLiteInterface
sqldb = SQLiteInterface('/Users/parsashemirani/Main/dastyaar/app/tools/filebase_test.db')

"""


"""
from app.tools.file_functions import extract_hash_from_filename as fhash
james = fhash('/Users/parsashemirani/Main/Inbox/DSC00919-v1-676a8b02fcc5a7012551da8a084fae35e6a273b55594c5d72053f7adf25c88c7.JPG')

"""



"""
from app.tools.file_functions import generate_new_filename as gnf
james = gnf(
    file_path='/Users/parsashemirani/Main/Inbox/DSC00919-v1-676a8b02fcc5a7012551da8a084fae35e6a273b55594c5d72053f7adf25c88c7.JPG',
    version_number=2,
    hash=b'|u\x18\x04\xcd\xa4\xabBt\xcf\xf2UI\xa6\xba~{\x83\t\xcbo\xd0\xb3x\xc6\x96\xbaLi\xebi\xe3'
)
"""