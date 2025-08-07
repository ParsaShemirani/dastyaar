from tools.models import StorageDevice
from tools.db import Session

NewDev = StorageDevice(
    name="testintakeonmac",
    size=12345,
    path="/Users/parsashemirani/Main/fakeintest"
)

with Session() as session:
    session.add(NewDev)
    session.commit()