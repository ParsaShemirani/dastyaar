from flask import Flask, request, jsonify
from app.tools.newsqliteinterface import SQLiteInterface
from app.tools.settings import FILEBASE_DB_FILE

interface = SQLiteInterface(database_path=FILEBASE_DB_FILE)

def dict_bin_to_hex(dictionary):
    out = {}
    for k, v in dictionary.items():
        if isinstance(v, bytes):
            out[k] = v.hex()
        else:
            out[k] = v
    return out


def create_app():
    app = Flask(__name__)

    @app.route("/execute_read", methods=['GET'])
    def execute_read():
        parameter_dict = {}
        parameter_dict['query'] = request.args.get('query')
        parameter_dict['params'] = request.args.get('params')
        parameter_dict['fetch_one'] = request.args.get('fetch_one')

        result = interface.execute_read(
            **{k: v for k, v in parameter_dict.items() if v is not None}
        )
        if parameter_dict['fetch_one'] == True:
            if result is None:
                return None
            else:
                result_dict = dict(result)
        else:
            result_dict = dict(result[0])
        safe_dict = dict_bin_to_hex(
            dictionary=result_dict
        )
        return jsonify(safe_dict)

    @app.route("/execute_write", methods=['POST'])
    def execute_write():
        data = request.get_json()

        parameter_dict = {}
        parameter_dict['query'] = data.get('query')
        parameter_dict['params'] = data.get('params')
        parameter_dict['many'] = data.get('many')
        print("PARAM DICT")
        print(parameter_dict)


        result = interface.execute_write(
            **{k: v for k, v in parameter_dict.items() if v is not None}
        )
        print("RESULT MAN")
        print(result)
        return 'Thanks for your support'
    return app

"""
from app.tools.flask_sqliteinterface import create_app
app = create_app()
app.run(host="0.0.0.0", port=5321)
"""

"""
import requests
input = {
    "query": "SELECT * FROM files ORDER BY id DESC LIMIT 1",
    "fetch_one": True
}
r = requests.get("http://127.0.0.1:5321/execute_read", params=input)
"""


"""
import requests
input = {
    "query": "SELECT * FROM files WHERE id=12343",
    "fetch_one": True
}
r = requests.get("http://127.0.0.1:5321/execute_read", params=input)
"""


####################### WRITE

"""
import requests
input = {
    "query": "INSERT INTO files_groupings (file_id, grouping_id) VALUES (?, ?)",
    "params": (352, 234)
}
r = requests.post("http://127.0.0.1:5321/execute_write", json=input)
"""