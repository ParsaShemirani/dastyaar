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

engine = create_engine(url_object, echo=True)

Session = sessionmaker(engine)
##########



with Session() as session:
    result = session.scalars(select(StorageDevice)).all()