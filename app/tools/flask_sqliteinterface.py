from flask import Flask, request, jsonify
from app.tools.sqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_DB_FILE

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

def create_app():
    app = Flask(__name__)

    @app.route("/execute_read", methods=['POST'])
    def execute_read():
        data = dict(request.get_json())
        data = convert_hex_to_binary(obj=data)
        db = SQLiteInterface(data['database_path'])
        
        result = db.execute_read(
            query=data['query'],
            params=data['params'],
            fetch_one=data['fetch_one']
        )
        result = convert_binary_to_hex(obj=result)
        return jsonify(result)


    @app.route("/jamietest", methods=['POST'])
    def jamie():
        data = request.get_json()
        print("DB PATH")
        print(data.get('database_path'))
        print("QUERY")
        print(data.get('query'))
        print("PARAMS")
        print(data.get('params'))
        print("FETCH_ONE")
        print(data.get('fetch_one'))
        print("FETCH ONE TYPE")
        print(type(data.get('fetch_one')))
        masterman = dict(data)
        print("SIMPLETON")
        print(masterman)
        return {"wickidman": 'thanks'}



    return app


"""
import requests

input = {
    "master": ['masterman', 234]
}


r = requests.post(
    url="http://127.0.0.1:5321/jamietest",
    json=input
)
"""









"""
from app.tools.flask_sqliteinterface import create_app
app = create_app()
app.run(host="0.0.0.0", port=5321)
"""

"""
import requests
input = {
    "query": "SELECT * FROM files ORDER BY id DESC LIMIT 3",
    "fetch_one": False
}
r = requests.get("http://127.0.0.1:5321/execute_read", params=input)
"""


"""
import requests
input = {
    "query": "SELECT * FROM files WHERE id=11234",
    "fetch_one": True
}
r = requests.get("http://127.0.0.1:5321/execute_read", params=input)
"""


####################### WRITE

"""
import requests
input = {
    "query": "INSERT INTO files_groupings (file_id, grouping_id) VALUES (?, ?)",
    "params": [(352, 234), (34543,234)],
    "many": True
}
r = requests.post("http://127.0.0.1:5321/execute_write", json=input)
"""