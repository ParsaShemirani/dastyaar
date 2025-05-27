from app.core.exceptions import DatabaseError
from .instance import filebase_instance
from typing import List, Dict, Any



def get_file_id_via_hash(sha_hash: str) -> int:
    """
    Get the ID of a file using its SHA hash.
    
    Args:
        sha_hash (str): The binary SHA-256 hash of the file
        
    Returns:
        int: The file ID if found, 0 if not found or error occurs
    """

    try:
        query = """
            SELECT 
                id 
            FROM files 
            WHERE hash = %s
        """
        result = filebase_instance.execute_read(query,[sha_hash],fetch_one=True)
        if result is None:
            return 0
        return result['id']

    except DatabaseError as e:
        # Re-raise the database error with more context
        raise DatabaseError(f"Failed to check has existence: {str(e)}")
    

def insert_file_location(file_id: int, location_name: str) -> bool:
    """
    Insert a new row for a file and its storage location using location name
    
    Args:
        file_id (int): The ID of the file
        location_name (str): The name of the location
        
    Returns:
        bool: True if insertion successful, False if failed
    """
    try:
        # First, verify the location exists
        check_query = """
            SELECT id FROM locations WHERE location = %s
        """
        location_result = filebase_instance.execute_read(check_query, [location_name], fetch_one=True)
        
        if location_result is None:
            raise DatabaseError(f"Location with name '{location_name}' not found")
        
        # Insert into file_location table using the location_id from the result
        insert_query = """
            INSERT INTO file_location
                (file_id, location_id)
            VALUES 
                (%s, %s)
        """
        filebase_instance.execute_write(insert_query, [file_id, location_result['id']])
        return True

    except DatabaseError as e:
        # Re-raise the database error with more context
        raise DatabaseError(f"Failed to insert file location: {str(e)}")
    

def get_version_number_via_hash(hash_value: bytes) -> int:
    """
    Get the version number of a file using its binary SHA hash.
    
    Args:
        hash_value (bytes): The binary SHA-256 hash of the file
        
    Returns:
        int: The version number if found, 0 if not found.
    """
    try:
        # Ensure the hash is in bytes format
        if not isinstance(hash_value, bytes):
            raise TypeError("hash_value must be bytes")
            
        query = """
            SELECT 
                version_number 
            FROM files 
            WHERE hash = %s
        """
        result = filebase_instance.execute_read(query, [hash_value], fetch_one=True)
        if result is None:
            return 0
        return result['version_number']
        
    except DatabaseError as e:
        # Re-raise the database error with more context
        raise DatabaseError(f"Failed to get version number: {str(e)}")
    


def insert_file(file_metadata: Dict[str, Any]) -> bool:
    """
    Insert a new file record into the database.

    Args:
        file_metadata (Dict[str, Any]): Dictionary containing file metadata    
    Returns:
        bool: True if insertion successful, False if failed
    """
    try:
        columns = ', '.join(file_metadata.keys())
        placeholders = ', '.join(['%s'] * len(file_metadata))
        query = f"""
            INSERT INTO files 
                ({columns}) 
            VALUES 
                ({placeholders})
        """
        values = tuple(file_metadata.values())
        filebase_instance.execute_write(query, values,False)
        return True

    except DatabaseError as e:
        # Re-raise the database error with more context
        raise DatabaseError(f"Failed to insert file: {str(e)}")
    
def search_files_description(search_text:str) -> List[Dict]:
    """
    Search for all fields of file entries using full text search on the "description"
    column.
    
    Args:
        search_text (str): The text to search for in file descriptions
        
    Returns:
        List[Dict]: A list of file records matching the search criteria, ordered by relevance
        
    Raises:
        DatabaseError: If there's an issue with the database query execution
    """
    try:
        query = """
        SELECT
            *,
            MATCH(description) AGAINST (%s IN NATURAL LANGUAGE MODE) AS relevance
        FROM files
        WHERE MATCH(description) AGAINST (%s IN NATURAL LANGUAGE MODE)
        ORDER BY relevance DESC
        """
        result = filebase_instance.execute_read(
            query=query,
            params=(search_text,search_text),
            fetch_one=False
        )
        return result
    except Exception as e:
        raise DatabaseError(f"An error occurred while fetching files: {str(e)}")

def insert_file_group(file_id: int, group_id: int) -> bool:
    """
    Insert a new row for a file and its group using group ID
    
    Args:
        file_id (int): The ID of the file
        group_id (int): The ID of the group
        
    Returns:
        bool: True if insertion successful, False if failed
    """
    try:
        # Insert into file_group junction table directly using the group_id
        insert_query = """
            INSERT INTO file_group
                (file_id, group_id)
            VALUES 
                (%s, %s)
        """
        filebase_instance.execute_write(insert_query, [file_id, group_id])
        return True

    except DatabaseError as e:
        # Re-raise the database error with more context
        raise DatabaseError(f"Failed to insert file group: {str(e)}")