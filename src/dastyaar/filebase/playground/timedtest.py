from dastyaar.filebase.models import File, VersionGroup, Edge
from dastyaar.filebase.connection import Session
from sqlalchemy import select
from sqlalchemy.orm import aliased

session = Session()

previous_file_hash = "aa7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

james = session.execute(
    select(File.id, File.version_number)
    .where(File.sha256_hash == previous_file_hash)
)