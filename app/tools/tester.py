from app.tools.filedata import FileData
from app.tools import filebase_functions as fbf
import pprint


def main(file_path):
    file_object = FileData(file_path=file_path)

    file_object.filld_hash() 

    print(file_object.is_unique())
    file_object.filld_size()
    file_object.filld_extension()
    # MANUAL MAN
    file_object.version_number = 1

    file_object.filld_basename()
    file_object.filld_rootname()

    file_object.filld_name()

    pprint.pprint(vars(file_object))


"""
from app.tools.tester import main as wicked
wicked('/Users/parsashemirani/Main/Inbox/trim_bells.m4a')

"""

"""
Version number logic:

If basename == rootname, then it does not have parent,
neither can hash be derived from basename.

so if basename == rootname, version_number = 1.

If they are different, we now need to use the hex hash value
which is in the basename to find its parent in the filebase,
get its version number, and incrememnt it.
"""