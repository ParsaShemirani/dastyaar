import subprocess
from app.tools import settings
from app.tools import read_sql_queries
import os


def scp_out(local_path, remote_user, remote_host, remote_path):
    command = ['scp', local_path, f'{remote_user}@{remote_host}:{remote_path}']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"SCP copy did not work {result.stderr.strip()}")

def scp_in(local_path, remote_user, remote_host, remote_path):
    command = ['scp', f'{remote_user}@{remote_host}:{remote_path}', local_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"SCP copy did not work {result.stderr.strip()}")


def scp_to_intake(file_path):
    scp_out(
        local_path=file_path,
        remote_user=settings.BONYAAD_COMPUTER_USER,
        remote_host=settings.BONYAAD_COMPUTER_HOST,
        remote_path=settings.INTAKE_DRIVE_PATH
    )

def scp_from_intake(file_name, local_path):
    location_path = read_sql_queries.get_location_path_via_file_name(
        file_name=file_name
    )
    scp_in(
        local_path=local_path,
        remote_user=settings.BONYAAD_COMPUTER_USER,
        remote_host=settings.BONYAAD_COMPUTER_HOST,
        remote_path=f"{location_path}{file_name}"
    )

################


def localize_file(file_id, local_path=settings.INGESTED_PATH):
    file_name = read_sql_queries.get_file_name_via_id(
        file_id=file_id
    )
    scp_from_intake(
        file_name=file_name,
        local_path=local_path
    )


def localize_grouping(grouping_id):
    grouping_name = read_sql_queries.get_grouping_name_via_id(
        grouping_id=grouping_id
    )
    directory = f"{settings.INGESTED_PATH}{grouping_name}"
    os.makedirs(directory)
    id_list = read_sql_queries.ids_in_grouping(
        grouping_id=grouping_id
    )
    for id in id_list:
        localize_file(
            file_id=id,
            local_path=directory
        )