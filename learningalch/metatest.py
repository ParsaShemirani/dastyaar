from sqlalchemy import MetaData, create_engine, URL

metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String

file_table = Table(
    "files",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("root_name", String(30)),
    Column("version_number", Integer)
)


guzsampletable = Table(
    "guzmans",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("tomatonumber", Integer),
    Column("toastman", String(234))
)




url_object = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="marioMaster65!",
    host="localhost",
    port=8432,
    database="filebase"
)

engine = create_engine(url_object, echo=True)


from sqlalchemy import select
stmt = select(file_table.c.id, file_table.c.version_number)