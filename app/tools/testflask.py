from flask import Flask, request, jsonify, send_file
from app.tools.sqlite_interface_client import SQLiteInterface
from app.tools.settings import FILEBASE_DB_FILE

from pprint import pprint
interface = SQLiteInterface(FILEBASE_DB_FILE)

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
    @app.route('/query', methods=['GET'])
    def execute_read():
        query = request.args.get('query')
        params = request.args.get('params')
        fetch_one = request.args.get('fetch_one')

        result = interface.execute_read(
            query=query,
            params=params,
            fetch_one=fetch_one
        )
        print("RESULT!!!!")
        print(result)
        print("dict(result)!!!!!")
        print(dict(result))

        unsafe_dict = dict(result)
        safe_dict = dict_bin_to_hex(unsafe_dict)

        print("UNSAFE DICT\n\n\n\n")
        pprint(unsafe_dict)
        print("SAFE DICT\n\n\n\n")
        pprint(safe_dict)
        jsonified = jsonify(safe_dict)
        print("JSONIFY SAFE DICT\n\n\n\n")
        pprint(jsonified)
        print("JSON DIR")
        pprint(dir(jsonified))
        print("JSON VARS")
        pprint(vars(jsonified))
        """
        print("NOW REAL STUFF:")
        pprint(request)
        print("DIR REQUEST")
        pprint(dir(request))
        print("VARS REQUEST")
        pprint(vars(request))
        print("GETTING DAAATA")
        pprint(request.get_data())
        
        """
        return "JAMIE"
    

    @app.route("/postman", methods=['POST'])
    def postman():
        print("THE REQUEST!")
        pprint(request)
        print("THE DIR")
        pprint(dir(request))
        print("THE VARS!")
        pprint(vars(request))
        print("JAMIEMAN DATA")
        print(request.get_data())
        return "thanks"
    
    
    @app.route('/imagetest', methods=['GET'])
    def imagetest():
        return send_file('/Users/parsashemirani/Main/ingested/C0055-v1-proxy.mp4')
    return app


"""
from app.tools.testflask import create_app
app = create_app()
app.run(host="0.0.0.0", port=5321)
"""

"""
import requests
params = {'query': 'SELECT * FROM files ORDER BY id DESC LIMIT ?', 'params': 1, 'fetch_one': 'False'}
r = requests.get("http://127.0.0.1:5321/query", params=params)
print(r.status_code)
print(r.json())
"""

"""
import requests
r = requests.get("http://127.0.0.1:5321/imagetest")
"""

"""
import requests
chicken = {'timidman': 123, 'secondjames': 'webb'}
r = requests.post("http://127.0.0.1:5321/postman", data=chicken)
"""







"""
import time
import requests
url = "http://192.168.1.5:5321/imagetest"
outfile = "/home/parsa/timidtest/proxyvid.mp4"

start = time.perf_counter()
r = requests.get(url, stream=True)

with open (outfile, 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

total_secs = time.perf_counter() - start
print(f'Full download + write took {total_secs} s')
"""