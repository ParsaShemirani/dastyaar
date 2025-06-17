import requests
from app.tools.settings import FILEBASE_DB_FILE
import json


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
    r = requests.get(
        url="http://127.0.0.1:5321/execute_read",
        params={
            "query": query,
            "params": json.dumps([values]),
            "fetch_one": False
        }
    )
    print("JUST R")
    print(r)
    print("CONTENT")
    print(r.content)
    print("JSON")
    print(r.json())
    print("STATUS QUO")
    print(r.status_code)

"""
from app.tools.testman import match_fdescription as mf
"""