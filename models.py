from __future__ import annotations


from datetime import datetime



from sqlalchemy import ForeignKey, Integer, BigInteger, String, CHAR,  Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(30))
    created_ts: Mapped[datetime] = mapped_column(DateTime)


    outgoing_relationships: Mapped[list[Relationship]] = relationship(
        "Relationship",
        foreign_keys="Relationship.source_id",
        back_populates="source_node",
    )

    incoming_relationships: Mapped[list[Relationship]] = relationship(
        "Relationship",
        foreign_keys="Relationship.target_id",
        back_populates="target_node"
    )



    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": "type"
    }


class Relationship(Base):
    __tablename__ = "relationships"

    source_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    type: Mapped[str]= mapped_column(String(50), primary_key=True)
    created_ts: Mapped[datetime] = mapped_column(DateTime)
    specific_metadata: Mapped[dict] = mapped_column(JSONB)

    source_node: Mapped[Node] = relationship(
        "Node",
        foreign_keys=[source_id],
        back_populates="outgoing_relationships"
    )

    target_node = relationship(
        "Node",
        foreign_keys=[target_id],
        back_populates="incoming_relationships"
    )









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

