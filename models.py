from __future__ import annotations

from typing import Any
from datetime import datetime, timezone

from sqlalchemy import (
    ForeignKey,
    Integer,
    BigInteger,
    String,
    CHAR,
    Text,
    DateTime,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import JSONB


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    type: Mapped[str] = mapped_column(String(30), init=False)
    created_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), init=False)

    # Edge relationships
    outgoing_relationships: Mapped[list[Edge]] = relationship(
        "Edge",
        foreign_keys="Edge.source_id",
        back_populates="source_node",
        init=False
    )

    incoming_relationships: Mapped[list[Edge]] = relationship(
        "Edge",
        foreign_keys="Edge.target_id",
        back_populates="target_node",
        init=False
    )

    # Joined table inheritance
    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": "type"
    }

class Edge(Base):
    __tablename__ = "edges"

    source_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True)
    type: Mapped[str]= mapped_column(String(50), primary_key=True)
    specific_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    created_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), init=False)

    # Node relationships
    source_node: Mapped[Node] = relationship(
        "Node",
        foreign_keys=[source_id],
        back_populates="outgoing_relationships",
        init=False
    )

    target_node: Mapped[Node] = relationship(
        "Node",
        foreign_keys=[target_id],
        back_populates="incoming_relationships",
        init=False
    )


class File(Node):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True, init=False)
    root_name: Mapped[str] = mapped_column(String(160))
    version_number: Mapped[int] = mapped_column(Integer)
    hash: Mapped[str] = mapped_column(CHAR(64))
    extension: Mapped[str] = mapped_column(String(16))
    size: Mapped[int] = mapped_column(BigInteger)
    ctime: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    specific_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    __mapper_args__ = {
        "polymorphic_identity": "file"
    }

class StorageDevice(Node):
    __tablename__ = "storage_devices"

    id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(160))
    size: Mapped[int] = mapped_column(BigInteger)

    __mapper_args__ = {
        "polymorphic_identity": "storage_device"
    }

class Collection(Node):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, default=None)

    __mapper_args__ = {
        "polymorphic_identity": "collection"
    }

