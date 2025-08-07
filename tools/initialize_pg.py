from tools.models import Base
from tools.db import engine


Base.metadata.create_all(engine)