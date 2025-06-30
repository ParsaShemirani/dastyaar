from mac_client.console import push_code
import ast


class SQLiteInterface:
    def __init__(self, database_path):
        self.database_path = database_path

    def execute_read(self, query, params=[], fetch_one=False):
        code = f"""
import server.sqliteinterface as db

result = db.execute_read(
    database_path="{self.database_path}",
    query='''{query}''',
    params={params},
    fetch_one={fetch_one}
)
print(result)
"""        
        result = push_code(code_str=code)
        decodedstring = result.decode('utf-8').strip()
        dict_or_list_form =  ast.literal_eval(decodedstring)
        return dict_or_list_form
    
    def execute_write(self, query, params=[], many=False):
        code = f"""
import server.sqliteinterface as db

result = db.execute_write(
    database_path="{self.database_path}",
    query='''{query}''',
    params={params},
    many={many}
)
print(result)
"""
        result = push_code(code_str=code)
        decodedstring = result.decode('utf-8').strip()
        return decodedstring



"""
from mac_client.sqlite_client import SQLiteInterface
db = SQLiteInterface('/home/parsa/serverfiles/filebase_test')
r = db.execute_read("SELECT name, extension FROM files WHERE id = 110", fetch_one=True)
"""

"""
from mac_client.read_filebase import get_file_name_via_id as gfnvi
j = gfnvi(31)
"""

"""
from mac_client.read_filebase import get_last_grouping_id as glgi
j = glgi()
"""