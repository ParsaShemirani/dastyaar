from app.tools.sqlite_client_interface import SQLiteInterface
from app.tools.settings import FILEBASE_DB_FILE


filebase_db = SQLiteInterface(FILEBASE_DB_FILE)

"""
IDEA: for a foundation, a group of funcitons that just return the file id
and the interested parameter that was searched for. 
"""

def match_fdescription(description):
    words = description.strip().split()
    values = " OR ".join(words)
    query = """
    SELECT files.id,
    fdescriptions.description,
    bm25(fdescriptions) AS relevance
    FROM files
    JOIN fdescriptions
    ON files.id = fdescriptions.file_id
    WHERE fdescriptions.description MATCH ?
    ORDER BY relevance ASC
    LIMIT 5
    """
    result = filebase_db.execute_read(
        query=query,
        params=[values],
        fetch_one=False
    )
    return result

def ids_in_grouping(grouping_id):
    query = """
    SELECT file_id
    FROM files_groupings
    WHERE grouping_id = ?
    """
    result = filebase_db.execute_read(
        query=query,
        params=[grouping_id],
        fetch_one=False
    )
    file_ids = [row['file_id'] for row in result]
    return file_ids

def get_file_name_via_id(file_id):
    query = """
    SELECT name
    FROM files
    WHERE id = ?
    """
    result = filebase_db.execute_read(
        query=query,
        params=[file_id],
        fetch_one=True
    )
    return result['name']

def match_gdescription(description):
    words = description.strip().split()
    values = " OR ".join(words)
    query = """
    SELECT groupings.name, groupings.id, gdescriptions.description,
    bm25(gdescriptions) AS relevance
    FROM groupings
    JOIN gdescriptions
    ON groupings.id = gdescriptions.grouping_id
    WHERE gdescriptions.description MATCH ?
    ORDER BY relevance ASC
    LIMIT 5
    """
    result = filebase_db.execute_read(
        query=query,
        params=[values],
        fetch_one=False
    )

    return result

def get_grouping_name_via_id(grouping_id):
    query = """
    SELECT name
    FROM groupings
    WHERE id = ?
    """
    result = filebase_db.execute_read(
        query=query,
        params=[grouping_id],
        fetch_one=True
    )
    return result['name']

def get_location_path_via_file_name(file_name):
    query = """
    SELECT locations.path
    FROM files
    JOIN files_locations ON files.id = files_locations.file_id
    JOIN locations ON files_locations.location_id = locations.id
    WHERE files.name = ?
    """
    result = filebase_db.execute_read(
        query=query,
        params=[file_name],
        fetch_one=True
    )
    return result['path']