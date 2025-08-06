from tools.models import Edge, File, StorageDevice, Collection


def ingest_file(file_path: str) -> None:
    db_file = File()
