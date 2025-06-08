from app.tools.file_utilities import file_functions
from app.tools.sqldb.db_interface import SQLiteInterface
from app.config.settings import FILEBASE_FILE

filebase_db = SQLiteInterface(FILEBASE_FILE)

def get_version_number(hash_value):
    query = """
    SELECT 
        version_number 
    FROM files 
    WHERE hash = ? 
    """
    result = filebase_db.execute_read(
         query=query,
         params=(hash_value,),
         fetch_one=True
    )
    if result:
         return result['version_number']
    return None

