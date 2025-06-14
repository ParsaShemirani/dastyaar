import subprocess
from app.tools import settings



def scp_out(local_path, remote_user, remote_host, remote_path):
    command = ['scp', local_path, f'{remote_user}@{remote_host}:{remote_path}']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"SCP copy did not work {Exception}")

def scp_in(local_path, remote_user, remote_host, remote_path):
    command = ['scp', f'{remote_user}@{remote_host}:{remote_path}', local_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"SCP copy did not work {Exception}")


def scp_to_intake(file_path):
    scp_out(
        local_path=file_path,
        remote_user=settings.BONYAAD_COMPUTER_USER,
        remote_host=settings.BONYAAD_COMPUTER_HOST,
        remote_path=settings.INTAKE_DRIVE_PATH
    )

def scp_from_intake(file_name, local_path):
    scp_in(
        local_path=local_path,
        remote_user=settings.BONYAAD_COMPUTER_USER,
        remote_host=settings.BONYAAD_COMPUTER_HOST,
        remote_path=f"{settings.INTAKE_DRIVE_PATH}{file_name}"
    )






    