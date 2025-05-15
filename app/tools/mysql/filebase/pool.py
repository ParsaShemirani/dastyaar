from app.core.dbpool import MySQLPoolInterface
from app.config import settings

_FILEBASE_DB_CONFIG = {
    'host': settings.MYSQL_HOST,
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'database': 'filebase'
}


filebase_pool = MySQLPoolInterface(
    config=_FILEBASE_DB_CONFIG,
    pool_name="filebase_pool",
    pool_size=5,
)
