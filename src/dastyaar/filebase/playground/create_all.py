from dastyaar.filebase.models import Base
from dastyaar.filebase.connection import engine

Base.metadata.create_all(bind=engine)