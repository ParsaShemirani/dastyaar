from server.sqliteinterface import SQLiteInterface

filebase_db = SQLiteInterface('/home/parsa/serverfiles/filebase_test.db')


def insert_file(file_dict):
    filtered_dict = {k: v for k, v in file_dict.items() if not k.startswith('_')}

    columns = ', '.join(filtered_dict.keys())
    placeholders = ', '.join(['?'] * len(filtered_dict))
    query = f"""
    INSERT INTO files 
         ({columns}) 
    VALUES 
         ({placeholders})
    """
    values = list(filtered_dict.values())

    filebase_db.execute_write(
         query=query,
         params=values,
         many=False
    )

def update_file(file_id, file_dict):
    filtered_dict = {k: v for k, v in file_dict.items() if not k.startswith('_')}

    set_clause = ', '.join([f"{key} = ?" for key in filtered_dict.keys()])
    query = f"""
    UPDATE files
    SET {set_clause}
    WHERE id = ?
    """
    values = list(filtered_dict.values()) + [file_id]

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

def create_grouping(name, _type_):
    query = """
    INSERT INTO groupings
    (name, type)
    VALUES
    (?, ?)
    """
    values = [name, _type_]

    filebase_db.execute_write(
        query=query,
        params=values,
        many=False
    )











