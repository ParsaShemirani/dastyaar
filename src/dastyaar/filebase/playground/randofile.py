from dastyaar.filebase.models import File
from dastyaar.filebase.connection import Session
from sqlalchemy import select
from pathlib import Path

from datetime import datetime, timezone

def randoinsert():
    file = File(
        root_name="GuZED OUt",
        version_number=123,
        sha256_hash="f0f299be320770be16866f000c4abc027e7806de57fac222ee22c52a202dc81a",
        extension=".guz",
    )
    with Session() as session:
        with session.begin():
            session.add(file)
            james = file.id

    return james

def foundmen():
    with Session() as session:
        chicken = session.scalar(select(File).where(File.sha256_hash == "f1f299be320770be16866f000c4abc027e7806de57fac222ee22c52a202dc81a"))

    return chicken

file = File(
    root_name="GuZED OUt",
    version_number=123,
    sha256_hash="f0f299be320770be16866f000c4abc027e7806de57fac222ee22c52a202dc81a",
    extension=".guz",
    size=1230493
)

with Session() as session:
    with session.begin():
        file.created_ts = datetime.now(timezone.utc)
        file.jamievar = "HELO JAMES"
        file.testfield = "jamietowned"
        session.add(file)
    session.refresh(file)

james = select(File).where