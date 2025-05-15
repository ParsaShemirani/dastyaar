from app.core.dbpool import MySQLPoolInterface
from app.config import settings

_JOURNALBASE_DB_CONFIG = {
    'host': settings.MYSQL_HOST,
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'database': 'journalbase'
}


journalbase_pool = MySQLPoolInterface(
    config=_JOURNALBASE_DB_CONFIG,
    pool_name="journalbase_pool",
    pool_size=5,
)
