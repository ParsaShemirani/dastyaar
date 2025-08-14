from dastyaar.filebase.models import VersionGroup
from dastyaar.filebase.connection import Session

with Session() as session:
    with session.begin():
        version_group = VersionGroup(
            head_file_id=2,
            origin_file_id=3
        )
        session.add(version_group)