from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE

filebase_db = SQLiteInterface(FILEBASE_FILE)

#### SINCE SQLITE USES TEXT BASED DATES ANYWAYS, REMOVE
#### TS PRECISION COLUMN AND PUT X MARKS ON UNPRECISE.

def get_version_number_via_hash(hash):
    query = """
    SELECT 
        version_number 
    FROM files 
    WHERE hash = ? 
    """
    result = filebase_db.execute_read(
         query=query,
         params=(hash,),
         fetch_one=True
    )
    if result is None:
         return 0
    return result['version_number']

def get_file_id_via_hash(hash):
     query = """
     SELECT
          id
     FROM files
     WHERE hash = ?
     """
     result = filebase_db.execute_read(
          query=query,
          params=(hash,),
          fetch_one=True
     )
     if result is None:
          return None
     return result['id']

def insert_file(file_dict):
     columns = ', '.join(file_dict.keys())
     placeholders = ', '.join(['?'] * len(file_dict))
     query = f"""
     INSERT INTO files 
          ({columns}) 
     VALUES 
          ({placeholders})
     """
     values = tuple(file_dict.values())
     result = filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )
