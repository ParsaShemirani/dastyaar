from datetime import datetime


from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg://postgres:marioMaster65!@localhost:8432/filebase", echo=True)

from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM files"))






from sqlalchemy import select
from sqlalchemy.orm import Session

from tools.filebase.models import File
"""
f1 = File(
    name="file1.txt",
    created_ts=datetime(2023,1,1),
    ingested_ts=datetime.now(),
    version_number=1,
    extension='txt',
size=12345,
sha256_hash="4485a2abb03152693603aaa1544623b2a85dca1f6bac27a3d7e43f093f88fc19",
    description="testfile1"
)
with Session(engine) as session:
    session.add(f1)
    session.commit()
"""


with Session(engine) as session:
    files = session.scalars(select(File)).all()
