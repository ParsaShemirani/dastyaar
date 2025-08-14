from dastyaar.filebase.models import File
from dastyaar.filebase.connection import Session
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

with Session() as session:
    with session.begin():
        sample_file = File(
            root_name="jamie",
            version_number=13,
            sha256_hash="aa7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            extension="mp4",
            size=282342,
            created_ts=datetime.now(tz=timezone.utc)
        )
        session.add(sample_file)