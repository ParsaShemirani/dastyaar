from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_FILE
from pprint import pprint

filebase_db = SQLiteInterface(FILEBASE_FILE)


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
    print("\n\n\n")

    for row in result:
        pprint(dict(row))
    return result

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
    for row in result:
        pprint(dict(row))

    return result


"""
from app.tools.sqlgroupings import make_new_grouping as mng
from app.tools.sqlgroupings import match_gdescription as mg
"""