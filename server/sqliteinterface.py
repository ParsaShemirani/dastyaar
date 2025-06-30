import sqlite3

class SQLiteInterface:
    def __init__(self, database_path):
        self.database_path = database_path

    def execute_read(self, query, params=[], fetch_one=False):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                return dict(row) if row else None
            else:
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        finally:
            cursor.close()
            connection.close()

    def execute_write(self, query, params=[], many=False):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        try:
            if many:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            connection.close()