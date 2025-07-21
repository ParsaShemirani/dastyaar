# models.py
from __future__ import annotations
from typing import Optional, List
from datetime import datetime

from sqlalchemy import (
    String, Integer, BigInteger, DateTime, Text, ForeignKey, Column
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)


# --- Base Class ---
class Base(DeclarativeBase):
    pass

# --- Association Table: files_groupings ---
from sqlalchemy import Table

files_groupings = Table(
    "files_groupings",
    Base.metadata,
    Column("file_id", ForeignKey("files.id"), primary_key=True),
    Column("grouping_id", ForeignKey("groupings.id"), primary_key=True),
)

# --- Association Table: files_storage_devices ---
files_storage_devices = Table(
    "files_storage_devices",
    Base.metadata,
    Column("file_id", ForeignKey("files.id"), primary_key=True),
    Column("storage_device_id", ForeignKey("storage_devices.id"), primary_key=True),
)

# --- File Table ---
class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_ts: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ingested_ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    extension: Mapped[str] = mapped_column(String(16), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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
    type: Mapped[str] = mapped_column(String(32), nullable=False)
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
    capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Relationships
    files: Mapped[List[File]] = relationship(
        "File",
        secondary=files_storage_devices,
        back_populates="storage_devices",
    )