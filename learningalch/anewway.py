from typing import List
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class File(Base):
    __tablename__ = "guzzyfiles"

    id: Mapped[int] = mapped_column("james", BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    timidname: Mapped[str | None]
    monsterman: Mapped[int] = mapped_column("timidgumoz", BigInteger, nullable=False)

    timidrel: Mapped[Timid] = relationship(back_populates="guzack")


    def __repr__(self) -> str:
        return(f"User(name={self.name!r})")


class Timid(Base):
    __tablename__ = "timids"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    timidnamd: Mapped[str] = mapped_column(String(2342))




from sqlalchemy import MetaData, create_engine, URL



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
stmt = select(File).filter_by(monsterman=23121234)

from sqlalchemy import delete
stmt = delete(File).where(File.monsterman == 2134123)


from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)


moneyman = File(name='tony', monsterman=1231)

moneyman.timidrel.