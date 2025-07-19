from __future__ import annotations
from typing import List, Optional
from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DateTime,
    Text,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
import enum

# --- ENUM for Grouping Type ---
class GroupingType(enum.Enum):
    collection = "collection"
    version = "version"
    proxy = "proxy"
    take = "take"

# --- Base Class ---
class Base(DeclarativeBase):
    pass

# --- Association Table: files_groupings ---
from sqlalchemy import Table

files_groupings = Table(
    "files_groupings",
    Base.metadata,
    mapped_column("file_id", ForeignKey("files.id"), primary_key=True),
    mapped_column("grouping_id", ForeignKey("groupings.id"), primary_key=True),
)

# --- Association Table: files_storage_devices ---
files_storage_devices = Table(
    "files_storage_devices",
    Base.metadata,
    mapped_column("file_id", ForeignKey("files.id"), primary_key=True),
    mapped_column("storage_device_id", ForeignKey("storage_devices.id"), primary_key=True),
)

# --- File Model ---
class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_ts: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ingested_ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    extension: Mapped[str] = mapped_column(String(16), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    # Relationships
    groupings: Mapped[List[Grouping]] = relationship(
        "Grouping",
        secondary=files_groupings,
        back_populates="files",
    )
    storage_devices: Mapped[List[StorageDevice]] = relationship(
        "StorageDevice",
        secondary=files_storage_devices,
        back_populates="files",
    )

# --- Grouping Model ---
class Grouping(Base):
    __tablename__ = "groupings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[GroupingType] = mapped_column(Enum(GroupingType), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    files: Mapped[List[File]] = relationship(
        "File",
        secondary=files_groupings,
        back_populates="groupings",
    )

# --- Storage Device Model ---
class StorageDevice(Base):
    __tablename__ = "storage_devices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Relationships
    files: Mapped[List[File]] = relationship(
        "File",
        secondary=files_storage_devices,
        back_populates="storage_devices",
    )