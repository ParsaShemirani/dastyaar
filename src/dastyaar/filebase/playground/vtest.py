from dastyaar.filebase.models import File, VersionGroup, Edge, Description
from dastyaar.filebase.connection import Session
from dastyaar.langchain.embeddings import generate_embedding
from sqlalchemy import select
from sqlalchemy.orm import aliased

session = Session()
"""
text = "This is an image of my sister and I at central park"

result = generate_embedding(text=text)

james = Description(
    text=text,
    embedding=result

)
"""

james = session.scalar(
    select(Description)
)