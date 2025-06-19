from app.tools.file_transfer_client import download_file
from app.tools.read_filebase import get_location_path_via_file_name, get_file_name_via_id, ids_in_grouping, get_grouping_name_via_id
from app.tools.settings import INGESTED_PATH
import os
def localize_file(file_id, local_directory):
    file_name = get_file_name_via_id(
        file_id=file_id
    )
    server_directory = get_location_path_via_file_name(
        file_name=file_name
    )
    server_file_path = f"{server_directory}{file_name}"

    download_file(
        server_file_path=server_file_path,
        local_directory=local_directory
    )

def localize_grouping(grouping_id):
    grouping_name = get_grouping_name_via_id(
        grouping_id=grouping_id
    )
    directory = f"{INGESTED_PATH}{grouping_name}"
    os.makedirs(directory)

    id_list = ids_in_grouping(
        grouping_id=grouping_id
    )
    for id in id_list:
        localize_file(
            file_id=id,
            local_directory=directory
        )