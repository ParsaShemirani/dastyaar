from dastyaar.filebase.models import File, VersionGroup, Edge
from dastyaar.filebase.connection import Session
from datetime import datetime, timezone
from sqlalchemy import select
session = Session()

session.begin()

file = session.scalar(select(File).where(File.id == 6))




for edge in file.outgoing_relationships:
    if edge.type == "in_version_group":
        previous_version_group = edge.target_node


print(previous_version_group.id)

print("JAMES\n\n\n\n\n\n\n\n")

print(previous_version_group.id)
