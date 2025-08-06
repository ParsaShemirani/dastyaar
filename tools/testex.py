from tools.models import Node, Edge, File, StorageDevice, Collection

from sqlalchemy import create_engine, URL, select
from sqlalchemy.orm import sessionmaker


url_object = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="marioMaster65!",
    host="localhost",
    port=8432,
    database="filebase"
)

engine = create_engine(url_object, echo=True)

Session = sessionmaker(engine)
##########

"""
with Session() as session:
    first_file = File(
        root_name="Jamieman",
        version_number=4,
        hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        extension="mp3",
        size=20311,
        ctime=None,
        specific_metadata=None,
        description="This is a random file I am using to test out the initiation"
    )
    session.add(first_file)
    session.commit()
"""

with Session() as session:
    first_file = session.scalar(select(File).filter_by(id=3))

    new_file = File(
        root_name="Jamieman",
        version_number=1234,
        hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b865",
        extension="mp3",
        size=20311,
        ctime=None,
        specific_metadata=None,
        description=None
    )

    linker = Edge(type="new_version_of", source_node=new_file, target_node=first_file)

    session.add_all([new_file, linker])
    session.commit()

