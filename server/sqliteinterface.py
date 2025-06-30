import sqlite3


def execute_read(database_path, query, params=[], fetch_one=False):
    connection = sqlite3.connect(database_path)
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

def execute_write(database_path, query, params=[], many=False):
    connection = sqlite3.connect(database_path)
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