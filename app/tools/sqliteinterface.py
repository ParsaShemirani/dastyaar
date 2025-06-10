import sqlite3

class SQLiteInterface:
    def __init__(self, database_path):
        self.database_path = database_path

    def connect(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
    
    def execute_read(self, query, params=(), fetch_one=False):
        self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                return row
            return cursor.fetchall()
        finally:
            cursor.close()
            self.connection.close()

    def execute_write(self, query, params=(), many=False):
        self.connect()
        cursor = self.connection.cursor()
        try:
            if many:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            self.connection.close()