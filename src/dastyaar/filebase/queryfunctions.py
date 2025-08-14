from dastyaar.filebase.models import File, Description
from sqlalchemy import func, select


select(Description).where(Description.tsv.match())