from flask import Flask, request, jsonify
from app.tools.newsqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_DB_FILE

interface = SQLiteInterface(database_path=FILEBASE_DB_FILE)

def bin_to_hex(obj):
    def convert(d):
        result = {}
        for k, v in d.items():
            result[k] = v.hex() if isinstance(v, (bytes, bytearray)) else v
        return result

    if isinstance(obj, dict):
        return convert(obj)
    if isinstance(obj, list):
        return [convert(d) for d in obj]



def create_app():
    app = Flask(__name__)

    @app.route("/execute_read", methods=['GET'])
    def execute_read():
        parameter_dict = {}
        parameter_dict['query'] = request.args.get('query')
        parameter_dict['params'] = request.args.get('params')
        fetch_one_arg = request.args.get('fetch_one')
        parameter_dict['fetch_one'] = str(fetch_one_arg).lower() == 'true'

        result = interface.execute_read(
            **{k: v for k, v in parameter_dict.items() if v is not None}
        )
        if result is None:
            return jsonify(result)
        else:
            safe_dict = bin_to_hex(result)
            return jsonify(safe_dict)

    @app.route("/execute_write", methods=['POST'])
    def execute_write():
        data = request.get_json()

        parameter_dict = {}
        parameter_dict['query'] = data.get('query')
        parameter_dict['params'] = data.get('params')
        many_arg = data.get('many')
        parameter_dict['many'] = str(many_arg).lower() == 'true'

        result = interface.execute_write(
            **{k: v for k, v in parameter_dict.items() if v is not None}
        )

        return jsonify({"rows_affected": result})
    return app

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