from app.config import settings
from typing import List, Dict, Any
import mysql.connector
from mysql.connector import Error


class FileDBManager:
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
                database="filebase",
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
    
    def check_hash_exists(self, sha_hash: str) -> bool:
        """
        Check if a file with the given SHA hash already exists in the database.
        
        Args:
            sha_hash (str): The SHA-256 hash of the file to check
            
        Returns:
            bool: True if the hash exists, False otherwise
        """
        try:
            self._ensure_connection()
            query = """
                SELECT 
                    COUNT(*) as count 
                FROM files 
                WHERE sha_hash = %s
            """
            self.cursor.execute(query, (sha_hash,))
            result = self.cursor.fetchone()
            return result['count'] > 0 if result else False
        except Error as e:
            print(f"Database error while checking hash: {e}")
            return False

    def insert_file(self, file_metadata: Dict[str, Any]) -> bool:
        """
        Insert a new file record into the database.
        
        Args:
            file_metadata (Dict[str, Any]): Dictionary containing file metadata
                Expected keys: filename, filepath, sha_hash, file_type, created_at
                
        Returns:
            bool: True if insertion successful, False if failed
        """
        if not file_metadata:
            print("Error: file_metadata cannot be empty")
            return False
            
        try:
            self._ensure_connection()
            columns = ', '.join(file_metadata.keys())
            placeholders = ', '.join(['%s'] * len(file_metadata))
            query = f"""
                INSERT INTO files 
                    ({columns}) 
                VALUES 
                    ({placeholders})
            """
            values = tuple(file_metadata.values())
            
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Successfully inserted file record into database")
            return True
        except Error as e:
            print(f"Database error during file insertion: {e}")
            self.connection.rollback()
            return False
        
    def get_file_id(self, sha_hash: str) -> int:
        """
        Get the ID of a file using its SHA hash.
        
        Args:
            sha_hash (str): The binary SHA-256 hash of the file
            
        Returns:
            int: The file ID if found, 0 if not found or error occurs
        """
        try:
            self._ensure_connection()
            query = """
                SELECT 
                    id 
                FROM files 
                WHERE sha_hash = %s
            """
            self.cursor.execute(query, (sha_hash,))
            result = self.cursor.fetchone()
            return result['id'] if result else 0
        except Error as e:
            print(f"Database error while getting file ID: {e}")
            return 0

    def insert_location(self, file_id: int, location_id: int) -> bool:
        """
        Insert a new row for a file and its storage location
        
        Args:
            file_id (int): The ID of the file
            location_id (int): The ID of the storage location
            
        Returns:
            bool: True if insertion successful, False if failed
        """
        if not file_id or not location_id:
            print("Error: Both file_id and location_id are required")
            return False
            
        try:
            self._ensure_connection()
            query = """
                INSERT INTO file_locations 
                    (file_id, location_id)
                VALUES 
                    (%s, %s)
            """
            self.cursor.execute(query, (file_id, location_id))
            self.connection.commit()
            print("Successfully inserted file-location mapping")
            return True
        except Error as e:
            print(f"Database error during location mapping insertion: {e}")
            self.connection.rollback()
            return False