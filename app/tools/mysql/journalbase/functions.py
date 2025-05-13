from app.config import settings
from typing import List, Dict, Any
import mysql.connector
from mysql.connector import Error


class JournalDBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database="journalbase",
                connection_timeout=5
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def _ensure_connection(self):
        """Ensure the connection is alive, reconnect if needed"""
        try:
            if not self.connection or not self.connection.is_connected():
                self._connect()
        except Error as e:
            print(f"Error reconnecting to database: {e}")
            raise

    def __del__(self):
        """Cleanup database resources"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()


    def get_entries(self, search_text: str) -> List[Dict[str, Any]]:
        """
        Fetch entries from the database using a full text natural language search
        on the `entry` column, ordered by relevance.
        """
        try:
            self._ensure_connection()
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
            self.cursor.execute(sql, (search_text, search_text))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Database error: {e}")
            return []
        
    def insert_entry(self, entry_text: str, created_time: str, file_id: int) -> bool:
        """
        Insert a new entry into the database.
        
        Args:
            entry_text (str): The text content of the entry
            created_time (str): The timestamp of entry creation (YYYY-MM-DD HH:MM:SS format)
            file_id (int): The associated file ID
            
        Returns:
            bool: True if insertion successful, False if failed
        """
        if not entry_text or not created_time or not file_id:
            print("Error: All parameters are required")
            return False
            
        insertion = """
            INSERT INTO entries 
                (entry, created_at, filebase_id) 
            VALUES 
                (%s, %s, %s)
        """
        
        try:
            self._ensure_connection()
            self.cursor.execute(insertion, (entry_text, created_time, file_id))
            self.connection.commit()
            print(f"Successfully inserted entry into database")
            return True
        except Error as e:
            print(f"Database error during insertion: {e}")
            return False
