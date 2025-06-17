from app.tools.sqlite_client_interface import SQLiteInterface
from app.tools.settings import FILEBASE_DB_FILE

filebase_db = SQLiteInterface(FILEBASE_DB_FILE)


def insert_file(file_dict):
     columns = ', '.join(file_dict.keys())
     placeholders = ', '.join(['?'] * len(file_dict))
     query = f"""
     INSERT INTO files 
          ({columns}) 
     VALUES 
          ({placeholders})
     """
     values = list(file_dict.values())

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
     values = [file_id, location_id]

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_grouping(file_id, grouping_id):
     query = """
     INSERT INTO files_groupings
     (file_id, grouping_id)
     VALUES
     (?,?)
     """
     values = [file_id, grouping_id]

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_fdescription(file_id, description):
     query = """
     INSERT INTO fdescriptions
     (file_id, description)
     VALUES
     (?,?)
     """
     values = [file_id, description]

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
     values = [file_id,previous_id]

     filebase_db.execute_write(
          query=query,
          params=values,
          many=False
     )

def associate_gdescription(grouping_id, description):
    query = """
    INSERT INTO gdescriptions
    (grouping_id, description)
    VALUES
    (?,?)
    """
    values = [grouping_id, description]

    filebase_db.execute_write(
        query=query,
        params=values,
        many=False
    )

def create_grouping(name):
    query = """
    INSERT INTO groupings
    (name)
    VALUES
    (?)
    """
    values = [name]

    filebase_db.execute_write(
        query=query,
        params=values,
        many=False
    )











