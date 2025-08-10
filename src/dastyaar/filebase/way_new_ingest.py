"""Functions that provide the entry point for files into the filebase

Functions are defined to ingest a file with the universal metadata,
and build on top of that to automate common workflows, such as ingesting
a file with an added description, file as part of collection, etc.
"""

import re
from typing import NamedTuple
from pathlib import Path
from hashlib import file_digest

from sqlalchemy import select
from sqlalchemy.orm import Session as SessionType

from dastyaar.settings import intake_path
from dastyaar.filebase.connection import Session
from dastyaar.filebase.models import Edge, File, StorageDevice, Description

FILENAME_REGEX = r"^(?P<root_name>.+)-v(?P<version_number>\d+)-(?P<sha256_hash>[0-9a-fA-F]{64})(?:\.(?P<extension>.+))$"
SHA256_HASH_REGEX = r"[0-9a-fA-F]{64}"


class FilenameComponents(NamedTuple):
    """Stores filename components from FILENAME_REGEX pattern"""

    root_name: str
    version_number: int
    sha256_hash: str


def create_filename_components(filename: str) -> FilenameComponents:
    match = re.match(pattern=FILENAME_REGEX, string=filename)
    filename_components = FilenameComponents(
        root_name=match.group("root_name"),
        version_number=int(match.group("version_number")),
        sha256_hash=match.group("sha256_hash"),
    )
    return filename_components


def generate_sha256_hash(file_path: Path) -> str:
    with file_path.open("rb") as f:
        return file_digest(f, "sha256").hexdigest()


def is_first_version(filename: str) -> bool:
    if re.search(pattern=SHA256_HASH_REGEX, string=filename):
        return False
    else:
        return True


def file_exists(sha256_hash: str, session: SessionType) -> bool:
    existing_file = session.scalar(select(File).where(File.sha256_hash == sha256_hash))
    return True if existing_file else False


def generate_new_filename(
    root_name: str, version_number: int, sha256_hash: str, extension: str
):
    if extension == "":
        new_filename = Path(f"{root_name}-v{version_number}-{sha256_hash}")
    else:
        new_filename = Path(f"{root_name}-v{version_number}-{sha256_hash}.{extension}")
    return new_filename


def create_first_version_file(file_path: Path, session: SessionType) -> File:
    sha256_hash = generate_sha256_hash(file_path=file_path)
    if file_exists(sha256_hash=sha256_hash, session=session):
        raise FileExistsError(f"File with hash {sha256_hash} already exists.")

    root_name = file_path.stem
    version_number = 1
    size = file_path.stat().st_size
    extension = file_path.suffix.lstrip(".").lower()

    file = File(
        root_name=root_name,
        version_number=version_number,
        sha256_hash=sha256_hash,
        extension=extension,
        size=size,
    )
    return file


def create_new_version_file_and_edge(
    file_path: Path, session: SessionType
) -> tuple[File, Edge]:
    sha256_hash = generate_sha256_hash(file_path=file_path)
    if file_exists(sha256_hash=sha256_hash, session=session):
        raise FileExistsError(f"File with hash {sha256_hash} already exists.")

    filename_components = create_filename_components(filename=file_path.name)
    previous_file = session.scalar(
        select(File).where(File.sha256_hash == filename_components.sha256_hash)
    )

    root_name = filename_components.root_name
    version_number = previous_file.version_number + 1
    size = file_path.stat().st_size
    extension = file_path.suffix.lstrip(".").lower()

    file = File(
        root_name=root_name,
        version_number=version_number,
        sha256_hash=sha256_hash,
        extension=extension,
        size=size,
    )
    edge = Edge(type="new_version_of", source_node=file, target_node=previous_file)
    return file, edge


def create_file_description_and_edge(
    file: File, description_text: str
) -> tuple[Description, Edge]:
    description = Description(text=description_text)
    edge = Edge(type="description_of", source_node=file, target_node=description)
    return description, edge


def create_intake_edge(file: File, intake_path: Path, session: SessionType) -> Edge:
    storage_device = session.scalar(
        select(StorageDevice).where(StorageDevice.path == str(intake_path))
    )
    if not storage_device:
        raise ValueError(
            f"Intake device not found in filebase. (intake_path: {str(intake_path)})"
        )

    return Edge(type="stored_on", source_node=file, target_node=storage_device)


def associate_storage_device(file: File, storage_device: StorageDevice) -> Edge: ...
