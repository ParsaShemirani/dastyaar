from typing import List, Dict, Any
from app.core.exceptions import DatabaseError
from .pool import journalbase_pool

def get_entries(search_text: str):
    """
    Fetch entries from the database using a full text natural language search
    on the `entry` column, ordered by relevance.
    """
    try:
        query = """
        SELECT
        id,
        entry,
        created_at,
        MATCH(entry) AGAINST (%s IN NATURAL LANGUAGE MODE) AS relevance
        FROM entries
        WHERE MATCH(entry) AGAINST (%s IN NATURAL LANGUAGE MODE)
        ORDER BY relevance DESC
        """
        result = journalbase_pool.execute_read(
            query=query, 
            params=(search_text,search_text),
            fetch_one=False
            )
        return result
    except Exception as e:
        raise DatabaseError(f"An error occurred while fetching entries: {str(e)}")

def insert_entry(entry_text: str, created_time: str, file_id: int) -> bool:
    """
    Insert a new entry into the database
    Args:
        entry_text (str): The text content of the entry
        created_time (str): The timestamp of entry creation (YYYY-MM-DD HH:MM:SS format)
        file_id (int): The associated file ID
    
    Returns:
        bool: True if insertion successful, False if failed
    """
    insertion = """
        INSERT INTO entries 
            (entry, created_at, filebase_id) 
        VALUES 
            (%s, %s, %s)
    """
    try:
        result = journalbase_pool.execute_write(
            query=insertion,
            params=(entry_text, created_time, file_id),
            many=False
        )
        return True
    except Exception as e:
        raise DatabaseError(f"An error occurred while inserting entry: {str(e)}")