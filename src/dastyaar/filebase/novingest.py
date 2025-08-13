"""Functions that provide the entry point for files into the filebase

Functions are defined to ingest a file with the universal metadata,
and build on top of that to automate common workflows, such as ingesting
a file with an added description, file as part of collection, etc.
"""

import re
from typing import NamedTuple
from pathlib import Path
from hashlib import file_digest
from datetime import datetime, timezone
import shutil

from sqlalchemy import select
from sqlalchemy.orm import Session as SessionType

from dastyaar.settings import intake_storage_device_path
from dastyaar.filebase.connection import Session
from dastyaar.filebase.models import Edge, File, StorageDevice, Description

FILENAME_REGEX = (
    r"^(?P<root_name>.+)-(?P<sha256_hash>[0-9a-fA-F]{64})(?:\.(?P<extension>.+))$"
)


class FilenameComponents(NamedTuple):
    """Stores filename components from FILENAME_REGEX pattern"""

    root_name: str
    sha256_hash: str


def extract_filename_components(filename: str) -> FilenameComponents:
    match = re.match(pattern=FILENAME_REGEX, string=filename)
    if match:
        filename_components = FilenameComponents(
            root_name=match.group("root_name"), sha256_hash=match.group("sha256_hash")
        )
        return filename_components
    else:
        return None


def generate_sha256_hash(file_path: Path) -> str:
    with file_path.open("rb") as f:
        return file_digest(f, "sha256").hexdigest()


def file_is_unique(sha256_hash: str, session: SessionType) -> bool:
    existing_file = session.scalar(select(File).where(File.sha256_hash == sha256_hash))
    return False if existing_file else True


def generate_new_filename(root_name: str, sha256_hash: str, extension: str) -> str:
    stem = f"{root_name}-{sha256_hash}"
    if extension == "":
        new_filename = stem
    else:
        new_filename = stem + "." + extension
    return new_filename


def create_file(file_path: Path, created_ts: datetime | None) -> File:
    filename_components = extract_filename_components(filename=file_path.name)
    if filename_components:
        root_name = filename_components.root_name
    else:
        root_name = file_path.stem

    sha256_hash = generate_sha256_hash(file_path=file_path)
    size = file_path.stat().st_size
    extension = file_path.suffix.lstrip(".").lower()
    if created_ts is None:
        created_ts = datetime.now(tz=timezone.utc)

    file = File(
        root_name=root_name,
        sha256_hash=sha256_hash,
        extension=extension,
        size=size,
        created_ts=created_ts,
    )
    return file


def ingest_file(file_path: Path, created_ts: datetime | None):
    file = create_file(file_path=file_path, created_ts=created_ts)
    with Session() as session:
        with session.begin():
            session.add(file)
        session.refresh(file)
    return file


def base_ingest(file_path: Path, created_ts: datetime | None) -> File:
    with Session() as session:
        with session.begin():
            sha256_hash = generate_sha256_hash(file_path=file_path)
            if not file_is_unique(sha256_hash=sha256_hash, session=session):
                raise FileExistsError(
                    f"File already exists in filebase. (sha256 hash: {sha256_hash})"
                )

            file = create_file(file_path=file_path, created_ts=created_ts)
            intake_storage_device = session.scalar(
                select(StorageDevice).where(
                    StorageDevice.path == str(intake_storage_device_path)
                )
            )
            intake_storage_device_edge = Edge(
                type="stored_on", source_node=file, target_node=intake_storage_device
            )
            filename_components = extract_filename_components(filename=file_path.name)
            if filename_components:
                previous_version_file = session.scalar(
                    select(File).where(
                        File.sha256_hash == filename_components.sha256_hash
                    )
                )
                new_version_edge = Edge(
                    type="new_version_of",
                    source_node=file,
                    target_node=previous_version_file,
                )
                session.add_all(
                    [
                        file,
                        intake_storage_device_edge,
                        new_version_edge,
                    ]
                )
            else:
                session.add_all(
                    [file, intake_storage_device_edge]
                )
        session.refresh(file)

    shutil.move(src=str(file_path), dst=str(intake_storage_device_path / file.sha256_hash))
    return file


"""
Put in higher level

    sha256_hash = generate_sha256_hash(file_path=file_path)
    if not file_is_unique(sha256_hash=sha256_hash, session=session):
        raise FileExistsError(
            f"File already exists in filebase. (sha256 hash: {sha256_hash})"
        )

"""
