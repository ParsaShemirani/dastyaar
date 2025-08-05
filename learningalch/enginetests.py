from sqlalchemy import create_engine, URL, text
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


"""
with engine.begin() as connection:
    result = connection.execute(
        text("INSERT INTO files (id, root_name, version_number) VALUES (:id, :root_name, :version_number)"),
        [
            {"id": 2, "root_name": "timothyguz", "version_number": 3423},
            {"id": 3, "root_name": "maniquendf", "version_number": 2342}
        ]
        )
"""



"""
with engine.connect() as connection:
    result = connection.execute(
        text("SELECT id, root_name, version_number FROM files")
    )
"""

Session = sessionmaker(engine)



with Session() as session:
    result = session.execute(
        text("SELECT id, root_name, version_number FROM files")
    )




"""
with Session.begin() as session:
    result = session.execute(
        text("INSERT INTO files (id, root_name, version_number) VALUES (:id, :root_name, :version_number)"),
        [
            {"id": 2, "root_name": "timothyguz", "version_number": 3423},
            {"id": 3, "root_name": "maniquendf", "version_number": 2342}
        ]
        )

"""



"""
with Session.begin() as session:
    result = session.execute(
        text("DELETE FROM files")
        )
        """

with engine.connect() as conn:
    conn.execute(text(
        """\
INSERT INTO guzzyfiles (name, timidgumoz)
VALUES (:name, :monsterman)
"""
    ),
    {"name": "samigozd", "monsterman": 1111234}
    )

    conn.commit()