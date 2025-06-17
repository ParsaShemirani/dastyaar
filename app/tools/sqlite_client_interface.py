import requests
from app.tools.settings import FILEBASE_DB_FILE
hosted_url = 'http://192.168.1.4:8000/'

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



class SQLiteInterface():
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
    
    def execute_write(self, query, params=[], many=False):
        data = {
            "database_path": self.database_path,
            "query": query,
            "params": params,
            "many": many
        }
        data = convert_binary_to_hex(obj=data)
        result = requests.post(
            url=f"{hosted_url}execute_write",
            json=data
        )
        result = result.json()
        affected_rows = result['affected_rows']
        return affected_rows




