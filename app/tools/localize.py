from app.tools import file_functions
from app.tools import read_sql_queries
import os
from app.tools.settings import INTAKE_DRIVE_PATH
ingested_folder = "/Users/parsashemirani/Main/ingested/"

def localize_file(file_id, local_folder=ingested_folder):
    file_name = read_sql_queries.get_file_name_via_id(
        file_id=file_id
    )
    result = file_functions.scp_from_bonyaad(
        local_path=local_folder,
        remote_user='parsa',
        remote_host='192.168.1.4',
        remote_path=f'{INTAKE_DRIVE_PATH}{file_name}'
    )
    return result


def localize_grouping(grouping_id):

    grouping_name = read_sql_queries.get_grouping_name_via_id(
        grouping_id=grouping_id
    )
    
    directory = f"{ingested_folder}{grouping_name}"

    os.makedirs(directory)


    id_list = read_sql_queries.ids_in_grouping(
        grouping_id=grouping_id
    )
    for id in id_list:
        localize_file(
            file_id=id,
            local_folder=directory
        )
