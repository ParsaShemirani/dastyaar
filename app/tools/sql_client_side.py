import requests
from app.tools.settings import FILEBASE_DB_FILE
hosted_url = 'http://127.0.0.1:5321/'

def convert_binary_to_hex(obj):
    if isinstance(obj, bytes):
        return {"_type": "hex", "data": obj.hex()}
    elif isinstance(obj, list):
        return [convert_binary_to_hex(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_binary_to_hex(value) for key, value in obj.items()}
    else:
        return obj
    
def convert_hex_to_binary(obj):
    if isinstance(obj, dict):
        if obj.get("_type") == "hex" and "data" in obj:
            return bytes.fromhex(obj["data"])
        else:
            return {key: convert_hex_to_binary(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_hex_to_binary(item) for item in obj]
    else:
        return obj



class clientsql():
    def __init__(self, database_path):
        self.database_path = database_path

    def execute_read(self, query, params=[], fetch_one=False):
        data = {
            "database_path": self.database_path,
            "query": query,
            "params": params,
            "fetch_one": fetch_one
        }
        data = convert_binary_to_hex(obj=data)
        result = requests.post(
            url=f"{hosted_url}execute_read",
            json=data
        )
        result = result.json()
        result = convert_hex_to_binary(obj=result)
        return result
    




jamie_db = clientsql(database_path=FILEBASE_DB_FILE)

def get_file_name_via_id(file_id):
    query = """
    SELECT name
    FROM files
    WHERE id = ?
    """
    result = jamie_db.execute_read(
        query=query,
        params=[file_id],
        fetch_one=True
    )
    print(result)


def masterman(file_id):
    query = """
    SELECT *
    FROM files
    WHERE hash = ?
    """
    values = [b"\x14]%\xacF\x82\xebn&\xe7J\x1a\xe2\x89\x1d\xd8\x97\x02\xcb..'\xceJ$R[\x00\xe7\xda\n\xe6"]
    result = jamie_db.execute_read(
        query=query,
        params=values
    )

    print(result)




"""
from app.tools.sql_client_side import get_file_name_via_id as gf
from app.tools.sql_client_side import masterman as mm
"""