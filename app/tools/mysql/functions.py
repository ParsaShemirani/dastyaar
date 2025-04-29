from app.config.settings import settings
from typing import List, Dict, Any
import mysql.connector
from mysql.connector import Error

def get_entries(search_text: str) -> List[Dict[str, Any]]:
    """
    Fetch entries from the database using a full text natural language search
    on the `entry` column, ordered by relevance.
    """
    try:
        # Database connection
        db = mysql.connector.connect(
            host=settings.mysql_host,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_db,
            connection_timeout=5
        )
        mysql_cursor = db.cursor(dictionary=True)
        try:
            sql = """
            SELECT
              id,
              entry,
              created_at,
              MATCH(entry) AGAINST (%s IN NATURAL LANGUAGE MODE) AS relevance
            FROM entries
            WHERE MATCH(entry) AGAINST (%s IN NATURAL LANGUAGE MODE)
            ORDER BY relevance DESC
            """
            mysql_cursor.execute(sql, (search_text, search_text))
            return mysql_cursor.fetchall()
        finally:
            mysql_cursor.close()
            db.close()
    except Error as e:
        # Log the error and re-raise or handle it appropriately
        print(f"Database error: {e}")
        return []