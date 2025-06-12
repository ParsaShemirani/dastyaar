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
    WHERE description MATCH ?
    ORDER BY relevance ASC
    LIMIT 5
    """
    result = filebase_db.execute_read(
        query=query,
        params=(values,),
        fetch_one=False
    )
    return result






"""
from app.tools.sqlqueries import match_description as md
from pprint import pprint
def o(james):
    for row in james:
        print("\nNEWMAN\n")
        pprint(dict(row))
"""

