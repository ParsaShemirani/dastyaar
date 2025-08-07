from sqlalchemy import select

from tools.db import Session
from tools.models import File, Edge, StorageDevice

session = Session()

stored_in_edges = session.scalars(
    select(Edge).where(Edge.type == "stored_in")
).all()


for edge in stored_in_edges:
    source_id = edge.source_id
    target_id = edge.target_id
    created_ts = edge.created_ts

    session.delete(edge)
    session.flush()

    jamie_source_node=session.scalar(select(File).where(File.id == source_id))
    jamie_target_node=session.scalar(select(StorageDevice).where(StorageDevice.id == target_id))

    session.flush()

    new_edge = Edge(
        type="stored_on",
        source_node=jamie_source_node,
        target_node=jamie_target_node
    )

    session.add(new_edge)

session.commit()