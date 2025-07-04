from server.sqliteinterface import SQLiteInterface

filebase_db = SQLiteInterface('/home/parsa/serverfiles/filebase_test.db')

file_id = 50


query = """
SELECT *
FROM files
WHERE id = ?
"""
file_dict = filebase_db.execute_read(
    query=query,
    params=[file_id],
    fetch_one=True
)



# Get groupings data
groupings_query = """
SELECT g.id, g.name, g.type
FROM groupings g
JOIN files_groupings fg ON g.id = fg.grouping_id
WHERE fg.file_id = ?
"""
groupings_result = filebase_db.execute_read(
    query=groupings_query,
    params=[file_id],
    fetch_one=False
)

file_dict['groupings'] = []
if groupings_result:
    for row in groupings_result:
        file_dict['groupings'].append({
            'id': row['id'],
            'name': row['name'],
            'type': row['type']
        })

# Get fdescription data
fdescription_query = """
SELECT file_id as id, description
FROM fdescriptions
WHERE file_id = ?
"""
fdescription_result = filebase_db.execute_read(
    query=fdescription_query,
    params=[file_id],
    fetch_one=True
)

if fdescription_result:
    file_dict['fdescription'] = {
        'id': fdescription_result['id'],
        'description': fdescription_result['description']
    }
else:
    file_dict['fdescription'] = None

# Get locations data
locations_query = """
SELECT l.id, l.name, l.path
FROM locations l
JOIN files_locations fl ON l.id = fl.location_id
WHERE fl.file_id = ?
"""
locations_result = filebase_db.execute_read(
    query=locations_query,
    params=[file_id],
    fetch_one=False
)

file_dict['locations'] = []
if locations_result:
    for row in locations_result:
        file_dict['locations'].append({
            'id': row['id'],
            'name': row['name'],
            'path': row['path']
        })

