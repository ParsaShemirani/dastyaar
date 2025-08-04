from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine("postgresql+psycopg://postgres:marioMaster65!@localhost:8432/filebase", echo=True)

session_factory = sessionmaker(bind=engine)

with session_factory() as session:
    #something here
    pass

with session_factory.begin() as session:
    #Do something besides select that needs commit here
    pass