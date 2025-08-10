from dastyaar.filebase.connection import Session
from dastyaar.filebase.models import StorageDevice

intake_device = StorageDevice(
    name="Wdmastermex",
    size=12345,
    path='/Users/parsashemirani/Main/fakeintest'
)
with Session() as session:
    with session.begin():
        session.add(intake_device)
    print("REMASTERED")
    session.refresh(intake_device)

from dastyaar.filebase.way_new_ingest import build_file_instance


