import re
from datetime import datetime, timezone
from pathlib import Path
from hashlib import file_digest
from typing import NamedTuple

from sqlalchemy import select
from sqlalchemy.orm import Session as SessionType, aliased

from dastyaar.filebase.models import Node, Edge, File, VersionGroup, Description
from dastyaar.langchain.embeddings import generate_embedding

FILENAME_REGEX = r"^(?P<root_name>.+)-v(?P<version_number>\d+)-(?P<sha256_hash>[0-9a-fA-F]{64})(?:\.(?P<extension>.+))$"


def generate_sha256_hash(file_path: Path) -> str:
    with file_path.open("rb") as f:
        return file_digest(f, "sha256").hexdigest()


class FilenameComponents(NamedTuple):
    """Stores filename components from FILENAME_REGEX pattern"""

    root_name: str
    version_number: int
    sha256_hash: str


def extract_filename_components(filename: str) -> FilenameComponents:
    match = re.match(pattern=FILENAME_REGEX, string=filename)
    if match:
        filename_components = FilenameComponents(
            root_name=match.group("root_name"),
            version_number=int(match.group("version_number")),
            sha256_hash=match.group("sha256_hash"),
        )
        return filename_components
    else:
        return None


def generate_new_filename(
    root_name: str, version_number: int, sha256_hash: str, extension: str
) -> str:
    stem = f"{root_name}-v{version_number}-{sha256_hash}"
    if extension == "":
        new_filename = stem
    else:
        new_filename = stem + "." + extension
    return new_filename


def handle_version_group(
    file: File, previous_sha256_hash: str, session: SessionType
) -> None:
    F = aliased(File, flat=True)
    version_group = session.scalar(
        select(VersionGroup)
        .select_from(F)
        .join(Edge, Edge.source_id == F.id)
        .join(VersionGroup, VersionGroup.id == Edge.target_id)
        .where(F.sha256_hash == previous_sha256_hash, Edge.type == "in_version_group")
    )
    previous_file = session.scalar(
        select(File).where(File.sha256_hash == previous_sha256_hash)
    )

    if version_group is None:
        if previous_file.version_number != 1:
            raise ValueError("Houston, we have a problem")
        version_group = VersionGroup()
        previous_file_version_edge = Edge(
            source_id=previous_file.id,
            target_id=version_group.id,
            type="in_version_group",
        )
        session.add_all([version_group, previous_file_version_edge])

    file.version_number = previous_file.version_number + 1
    file_version_edge = Edge(
        source_id=file.id, target_id=version_group.id, type="in_version_group"
    )
    session.add(file_version_edge)


def create_description(node: Node, text: str, session: SessionType) -> None:
    description = Description(text=text, embedding=generate_embedding(text=text))
    description_edge = Edge(
        source_id=node.id, target_id=description.id, type="has_description"
    )
    session.add_all([description, description_edge])


def ingest_file(
    file_path: Path,
    session: SessionType,
    created_ts: datetime | None,
    description_text: str | None = None,
) -> None:
    filename_components = extract_filename_components(filename=file_path.name)
    if filename_components:
        root_name = filename_components.root_name
        previous_sha256_hash = filename_components.sha256_hash
    else:
        root_name = file_path.stem
        previous_sha256_hash = None

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

    if previous_sha256_hash:
        handle_version_group(
            file=file, previous_sha256_hash=previous_sha256_hash, session=session
        )

    if description_text:
        create_description(node=file, text=description_text, session=session)