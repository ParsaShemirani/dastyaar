from models import Node, Edge, File, StorageDevice, Collection

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

engine = create_engine(url_object)

Session = sessionmaker(engine)
##########


"""
with Session() as session:
    maniquen = session.scalar(select(StorageDevice).where(StorageDevice.id == 1))
    maniout = maniquen.outgoing_relationships

    for item in maniout:
        if item.type == 'jamiestoredwashere':
            timbuk = item.target_node
    print("GUZIED TO BAZI! \n\n\n\n\n\n\n")
    print(timbuk)
"""


from datetime import datetime, timedelta

one_week_ago = datetime.now() - timedelta(days=7)

with Session() as session:
    first_file = session.scalar(
        select(Edge)
        .where(
            Edge.source_id == first
        )
    )

    found_file = first_file.outgoing_relationships[0].target_node
    print(found_file)
