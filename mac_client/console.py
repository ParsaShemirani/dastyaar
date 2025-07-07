import requests
import base64

console_host = "http://192.168.1.4:8321"
#Local server: http://192.168.1.4:8321

def push_code(code_str):
    utf8_bytes = code_str.encode('utf-8')
    
    b64_bytes = base64.b64encode(utf8_bytes)
    
    b64_string = b64_bytes.decode('ascii')
    
    transport_data = b64_string.encode('ascii')
    response = requests.post(
        f"{console_host}/console_push",
        data=transport_data
    )
    
    response_b64_decoded = base64.b64decode(response.content)
    result_string = response_b64_decoded.decode('utf-8')
    
    return result_string

def get_console_history_string():
    response = requests.get(f'{console_host}/console_history_string')
    
    history_b64_decoded = base64.b64decode(response.content)
    
    history_string = history_b64_decoded.decode('utf-8')
    
    return history_string

def reset_console():
    response = requests.post(url=f"{console_host}/reset_console")
    return response.status_code

def soft_reset():
    response = requests.post(url=f"{console_host}/soft_reset")
    return response.status_code

"""
from mac_client.new_console import push_code as pc, get_console_history_string as gc
""" 

"""
from mac_client.sqlite_client import SQLiteInterface
db = SQLiteInterface("/home/parsa/serverfiles/filebase_test.db")
r = db.execute_read("SELECT * FROM files WHERE id = 110")
"""