import re
import shutil
from pathlib import Path
from hashlib import file_digest
from datetime import datetime, timezone

from sqlalchemy import select

from settings import intake_path
from tools.db import Session
from tools.models import Edge, File, StorageDevice

filename_regex = r"^(?P<root_name>.+)-v(?P<version_number>\d+)-(?P<sha256_hash>[0-9a-fA-F]{64})(?:\.(?P<extension>.+))$"
potential_regex = r"[0-9a-fA-F]{30,}"

def ingest_file(file_path: Path, ctime: datetime) -> File:

    # Match regex pattern, assign root_name, old_version_number,
    # and old_sha256_hash
    if re.search(pattern=potential_regex, string=file_path.name):
        name_match = re.match(pattern=filename_regex, string=file_path.name)

        if name_match:
            root_name = name_match.group('root_name')
            old_version_number = int(name_match.group("version_number"))
            old_sha256_hash = name_match.group('sha256_hash')
        else:
            raise ValueError("Filename indicates potential ingestion before, but no filename structure regex match.")
    else:
        root_name = file_path.stem
        old_version_number = None
        old_sha256_hash = None

    # Generate and assign other values
    file_size = file_path.stat().st_size
    file_extension = file_path.suffix.lstrip('.').lower()
    version_number = old_version_number + 1 if old_version_number else 0
    with file_path.open("rb") as f:
        sha256_hash = file_digest(f, "sha256").hexdigest()

    # Generate new filename and rename the file
    if file_extension == "":
        new_filename = Path(f"{root_name}-v{version_number}-{sha256_hash}")
    else:
        new_filename = Path(f"{root_name}-v{version_number}-{sha256_hash}.{file_extension}")
    file_path.rename(target=new_filename)

    # Move file to intake directory
    shutil.move(src=new_filename, dst=intake_path)

    # Create file object with generated values
    FileInstance = File(
        root_name=root_name,
        version_number=version_number,
        sha256_hash=sha256_hash,
        extension=file_extension,
        size=file_size,
        ctime=ctime
    )

    with Session() as session:

        # Retrieve intake storage device, make edge to associate it to the new file
        IntakeDeviceInstance = session.scalar(select(StorageDevice).where(StorageDevice.path == str(intake_path)))
        StoredOnEdgeInstance = Edge(
            type="stored_on",
            source_node=FileInstance,
            target_node=IntakeDeviceInstance,
        )

        # Potentially retrieve previous version of file,
        # add all objects to database
        if old_sha256_hash:
            OldFileInstance = session.scalar(select(File).where(File.sha256_hash == old_sha256_hash))
            NewVersionEdge = Edge(
                type="new_version_of",
                source_node=FileInstance,
                target_node=OldFileInstance,
            )
            session.add_all([FileInstance, StoredOnEdgeInstance, OldFileInstance, NewVersionEdge])
        else:
            session.add_all([FileInstance, StoredOnEdgeInstance])
        session.commit()

        # Return the id of the newly inserted file
        session.refresh(FileInstance)
        return FileInstance

def ingest_server_file(file_path: Path) -> File:
    current_time = datetime.now(tz=timezone.utc)
    return ingest_file(file_path=file_path, ctime=current_time)

def ingest_client_file(file_path: Path, ctime: datetime, description: str | None = None) -> File:
    FileInstance = ingest_file(file_path=file_path, ctime=ctime)

    if not description:
        return FileInstance
    
    with Session() as session:
        FileInstance.description = description
        
        session.add(FileInstance)
        session.commit()


