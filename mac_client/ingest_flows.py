
from mac_client.pending_to_ingest import ingest_file
def ingest_one(file_path):
    version_number = ingest_file(
        file_path=file_path
    )
    