from app.tools.filedata import FileData
from app.tools import filebase_functions as fbf
from pprint import pprint


def main(file_path):
    file_object = FileData(file_path=file_path)

    file_object.filld_hash()
    print(file_object.is_unique())
    file_object.filld_basename()
    file_object.filld_rootname()
    file_object.filld_extension()
    file_object.filld_version_number()
    #file_object.version_number = 4
    file_object.filld_name()
    file_object.filld_size()
    file_object.filld_ts()

    print("Printing file attributes:\n")
    pprint(vars(file_object))

    file_dict = file_object.generate_file_dict()
    print("Printing file_dict:\n")
    pprint(file_dict)

    fbf.insert_file(file_dict=file_dict)



"""
from app.tools.tester import main as wicked
wicked('/Users/parsashemirani/Main/Inbox/DSC20021-v1-cd352285d1d4ea24a4bf8da44a4963a857e520c946310e8afc98ceb5d247c965.jpg')

"""
"""
from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE
from pprint import pprint
sqldb = SQLiteInterface(FILEBASE_FILE)
read = sqldb.execute_read
write = sqldb.execute_write
"""
