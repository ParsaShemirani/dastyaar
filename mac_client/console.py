import requests
console_host = "https://2ea6-2601-644-8f00-230-00-d0.ngrok-free.app"


def push_code(code_str):
        encoded_str = code_str.encode('utf-8')
        response = requests.post(
            f"{console_host}/console_push",
            data=encoded_str
        )
        return response.content

def get_console_history_string():
    response = requests.get(f'{console_host}/console_history_string')
    binary_object = response.content
    history_string = binary_object.decode('utf-8')
    return history_string

def reset_console():
      response = requests.post(url=f"{console_host}/reset_console")
      return response.status_code

def soft_reset():
      response = requests.post(url=f"{console_host}/soft_reset")
      return response.status_code

"""
from mac_client.console_client import push_code as pc, get_console_history_string as gc
""" 

"""
from mac_client.sqlite_client import SQLiteInterface
db = SQLiteInterface("/home/parsa/serverfiles/filebase_test.db")
r = db.execute_read("SELECT * FROM files WHERE id = 110")
"""