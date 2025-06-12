from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE

filebase_db = SQLiteInterface(FILEBASE_FILE)


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
        params=(values,),
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
        params=(grouping_id,),
        fetch_one=True
    )
    return result['name']




"""
from app.tools.sqlgroupings import make_new_grouping as mng
from app.tools.sqlgroupings import match_gdescription as mg
from app.tools.sqlgroupings import get_grouping_name_via_id as ggnvi
"""