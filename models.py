from datetime import datetime



from sqlalchemy import ForeignKey, Integer, BigInteger, String, CHAR,  Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(30))
    created_ts: Mapped[datetime] = mapped_column(DateTime)

    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": "type"
    }



class File(Node):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    root_name: Mapped[str] = mapped_column(String(160))
    version_number: Mapped[int] = mapped_column(Integer)
    hash: Mapped[str] = mapped_column(CHAR(64))
    extension: Mapped[str] = mapped_column(String(16))
    size: Mapped[int] = mapped_column(BigInteger)
    created_ts: Mapped[datetime] = mapped_column(DateTime)
    specific_metadata: Mapped[dict] = mapped_column(JSONB)
    description: Mapped[str] = mapped_column(Text)

    __mapper_args__ = {
        "polymorphic_identity": "file"
    }

class StorageDevice(Node):
    __tablename__ = "storage_devices"

    id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    size: Mapped[int] = mapped_column(BigInteger)

    __mapper_args__ = {
        "polymorphic_identity": "storage_device"
    }

class Collection(Node):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)

    __mapper_args__ = {
        "polymorphic_identity": "collection"
    }

class Relationship(Base):
    __tablename__ = "relationships"

    from_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    to_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    type: Mapped[str]= mapped_column(String(50))
    created_ts: Mapped[datetime] = mapped_column(DateTime)
    specific_metadata: Mapped[dict] = mapped_column(JSONB)