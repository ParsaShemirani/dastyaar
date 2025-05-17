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
    

def insert_file_location(file_id: int, location_id: int) -> bool:
    """
    Insert a new row for a file and its storage location
    
    Args:
        file_id (int): The ID of the file
        location_id (int): The ID of the storage location
        
    Returns:
        bool: True if insertion successful, False if failed
    """
    try:
        query = """
            INSERT INTO file_location
                (file_id, location_id)
            VALUES 
                (%s, %s)
        """
        filebase_instance.execute_write(query, [file_id, location_id])
        return True

    except DatabaseError as e:
        # Re-raise the database error with more context
        raise DatabaseError(f"Failed to insert file location: {str(e)}")
    

def get_version_number_via_hash(hash_value: str) -> int:
    """
    Get the version number of a file using its binary SHA hash.
    
    Args:
        hash_value (str): The binary SHA-256 hash of the file
        
    Returns:
        int: The version number if found, 0 if not found.
    """
    try:
        query = """
            SELECT 
                version_number 
            FROM files 
            WHERE hash = UNHEX(%s)
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