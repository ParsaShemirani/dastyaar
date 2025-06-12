from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE


filebase_db = SQLiteInterface(FILEBASE_FILE)

"""
IDEA: for a foundation, a group of funcitons that just return the file id
and the interested parameter that was searched for. 
"""

def match_description(description):
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
        params=(values,),
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
        params=(grouping_id,),
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
        params=(file_id,),
        fetch_one=True
    )
    return result['name']




"""
from app.tools.sqlqueries import match_description as md
from pprint import pprint
def o(james):
    for row in james:
        print("\nNEWMAN\n")
        pprint(dict(row))
"""

"""
from app.tools.sqlqueries import ids_in_grouping as iig
from app.tools.sqlqueries import get_file_name_via_id as gfnvi
"""