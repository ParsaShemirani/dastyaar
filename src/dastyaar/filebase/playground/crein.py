from dastyaar.filebase.connection import Session
from dastyaar.filebase.models import StorageDevice
from dastyaar.settings import intake_storage_device_path

intake_device = StorageDevice(
    name="Wdmastermex",
    size=12345,
    path=str(intake_storage_device_path)
)
with Session() as session:
    with session.begin():
        session.add(intake_device)
    print("REMASTERED")
    session.refresh(intake_device)

