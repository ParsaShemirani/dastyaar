from app.tools import read_filebase, write_filebase, settings, filedata, file_transfer_client
from app.tools.settings import INTAKE_DRIVE_PATH
import os
import textwrap
def description_search(description):
    result = read_filebase.match_txt_description(
        description=description
    )
    result_list = []
    for row in result:
        result_list.append(f"id: {row['id']}")
        result_list.append(f"description: {row['description']}")
        result_list.append("--------------")
        result_list.append("")
    return result_list
    
def make_text_sixty(text):
    collapsed = ' '.join(text.split())
    lines = textwrap.wrap(collapsed, width=60)
    return '\n'.join(lines)



def open_file(file_id):
    file_name = read_filebase.get_file_name_via_id(
        file_id=id
    )
    local_temp_directory = '/Users/parsashemirani/main/ingested'
    local_temp_file = os.path.join(local_temp_directory, file_name)

    file_transfer_client.download_file(
        server_file_path=f'{INTAKE_DRIVE_PATH}{file_name}',
        local_directory=local_temp_directory
    )
    with open(local_temp_file, 'r'_ as f):
        
