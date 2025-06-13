from app.tools import file_functions
from app.tools import read_sql_queries
ingested_folder = "/Users/parsashemirani/Main/ingested"

def localize_file(file_id, local_folder=ingested_folder):
    file_name = read_sql_queries.get_file_name_via_id(
        file_id=file_id
    )
    result = file_functions.scp(
        local_path=local_folder,
        remote_user='parsa',
        remote_host='192.168.1.4',
        remote_path=f'/mnt/wdhd/test_base/{file_name}',
        upload=False
    )
    return result