from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE

filebase_db = SQLiteInterface(FILEBASE_FILE)

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
         return None
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

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_location(file_id, location_id):
     query = """
     INSERT INTO files_locations
     (file_id, location_id)
     VALUES
     (?,?)
     """
     values = (file_id, location_id)

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_groupings(file_id, grouping_id):
     query = """
     INSERT INTO files_groupings
     (file_id, grouping_id)
     VALUES
     (?,?)
     """
     values = (file_id, grouping_id)

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_description(file_id, description):
     query = """
     INSERT INTO fdescriptions
     (file_id, description)
     VALUES
     (?,?)
     """
     values = (file_id, description)

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_previous_id(file_id, previous_id):
     query = """
     INSERT INTO previous_ids
     (file_id, previous_id)
     VALUES
     (?,?)
     """
     values = (file_id,previous_id)

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

# Groupings

def make_new_grouping(grouping_name, description):
    query = """
    INSERT INTO groupings
    (name)
    VALUES
    (?)
    """
    values = (grouping_name,)

    filebase_db.execute_write(
        query=query,
        params=values,
        many=False
    )

    id_fetch = filebase_db.execute_read(
        query="SELECT id FROM groupings ORDER BY id DESC LIMIT 1",
    )
    grouping_id = dict(id_fetch[0])['id']

    query = """
    INSERT INTO gdescriptions
    (grouping_id, description)
    VALUES
    (?,?)
    """
    filebase_db.execute_write(
        query=query,
        params=(grouping_id, description),
        many=False
    )

    query = """
    SELECT groupings.id, groupings.name, gdescriptions.description
    FROM groupings
    JOIN gdescriptions ON groupings.id = gdescriptions.grouping_id
    WHERE groupings.id = ?
    """
    result = filebase_db.execute_read(
        query=query,
        params=(grouping_id,),
        fetch_one=False
    )

    return result