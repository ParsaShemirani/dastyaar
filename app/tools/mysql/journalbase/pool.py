from app.core.dbinterface import MySQLInterface
from app.config import settings

_JOURNALBASE_DB_CONFIG = {
    'host': settings.MYSQL_HOST,
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'database': 'journalbase'
}

journalbase_pool = MySQLInterface(config=_JOURNALBASE_DB_CONFIG)
