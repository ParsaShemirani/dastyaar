from app.core.dbinterface import MySQLInterface
from app.config import settings

_FILEBASE_DB_CONFIG = {
    'host': settings.MYSQL_HOST,
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'database': 'filebase'
}

filebase_instance = MySQLInterface(config=_FILEBASE_DB_CONFIG)
