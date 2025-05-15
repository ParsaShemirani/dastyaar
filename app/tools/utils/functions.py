import hashlib
from typing import Union, Optional
from pathlib import Path
import os
import re
import datetime
import shutil


def generate_sha_hash(file_path: Union[str, Path], hex_output: bool = True) -> Union[str, bytes]:
    """
    Generate SHA-256 hash of a file.
    
    Args:
        file_path (Union[str, Path]): The path to the file to hash
        hex_output (bool, optional): If True, returns hex string. If False, returns bytes.
            Defaults to True.
            
    Returns:
        Union[str, bytes]: The SHA-256 hash of the file, either as hex string or bytes
        
    Raises:
        FileNotFoundError: If the specified file does not exist
        IOError: If there are issues reading the file
    """
    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)
            
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest() if hex_output else sha256_hash.digest()
        
    except (IOError, Exception) as e:
        print(f"Error generating SHA hash for {file_path}: {e}")
        raise


def get_file_size(full_path: Union[str, Path]) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        full_path (Union[str, Path]): The path to the file
        
    Returns:
        int: Size of the file in bytes
        
    Raises:
        FileNotFoundError: If the specified file does not exist
        OSError: If there are issues accessing the file
    """
    try:
        if isinstance(full_path, str):
            full_path = Path(full_path)
            
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")
            
        return os.path.getsize(full_path)
        
    except (OSError, Exception) as e:
        print(f"Error getting file size for {full_path}: {e}")
        raise


def extract_hash_from_filename(file_path: str) -> Optional[str]:
    """
    Extract binary SHA-256 hash from a filename that follows the pattern -v<number>-<hash>.
    
    Args:
        file_path (str): The file path or name to extract hash from
        
    Returns:
        Optional[str]: The binary sha-256 hash converted from hex if found, None otherwise
    """
    pattern = r'-v\d+-([a-f0-9]{64})(?:\.\w+)?$'
    match = re.search(pattern, file_path)
    
    hex_hash = match.group(1) if match else None
    
    if hex_hash:
        # Convert hex string to binary
        return bytes.fromhex(hex_hash).decode('utf-8')
            
    return None


def get_file_extension(full_path: str) -> str:
    """
    Extract and return the lowercase file extension from a file path.
    
    Args:
        full_path (str): The path to the file
        
    Returns:
        str: The lowercase file extension without the leading period,
             or empty string if no extension exists
    """
    _, ext = os.path.splitext(full_path)
    return ext[1:].lower() if ext else ''


def get_created_time(path: str) -> str:
    """
    Get the creation time of a file in MySQL DATETIME format.
    
    Args:
        path (str): The path to the file
        
    Returns:
        str: File creation time in 'YYYY-MM-DD HH:MM:SS' format
        
    Raises:
        FileNotFoundError: If the file does not exist
        OSError: If there are issues accessing file statistics
    """
    stat = os.stat(path)
    ctime = stat.st_birthtime if hasattr(stat, 'st_birthtime') else os.path.getctime(path)
    return datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')


def get_modified_time(path: str) -> str:
    """
    Get the last modification time of a file in MySQL DATETIME format.
    
    Args:
        path (str): The path to the file
        
    Returns:
        str: File modification time in 'YYYY-MM-DD HH:MM:SS' format
        
    Raises:
        FileNotFoundError: If the file does not exist
        OSError: If there are issues accessing file statistics
    """
    stat = os.stat(path)
    return datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')


def get_current_time() -> str:
    """
    Get the current time in MySQL DATETIME format.
    
    Returns:
        str: Current time in 'YYYY-MM-DD HH:MM:SS' format
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def generate_voicerec_filename(file_path: str, new_hash: str) -> str:
    """
    Generate a new filename for journal voice memo entries.
    
    Args:
        file_path (str): Current file path
        new_hash (str): Hash to be included in new filename        
    Returns:
        str: New filename with updated version and hash
    """
    base_name = os.path.basename(file_path)
    
    name, ext = os.path.splitext(base_name)
    journal_prefix = "journalbase_entry"
    return f"{journal_prefix}-v1-{new_hash}{ext}"


def get_new_full_path(current_path: str, new_name: str) -> str:
    """
    Construct the new full path for a file within the same directory.
    
    Args:
        current_path (str): Full path of the existing file
        new_name (str): New name for the file (without path)
        
    Returns:
        str: The new full path
        
    Raises:
        FileNotFoundError: If the source file does not exist
    """
    if not os.path.exists(current_path):
        raise FileNotFoundError(f"Source file {current_path} does not exist")
    
    directory = os.path.dirname(current_path)
    return os.path.join(directory, new_name)


def renamer(current_path: str, new_path: str) -> str:
    """
    Safely rename a file from the current path to the new path.
    
    Args:
        current_path (str): Full path of the existing file
        new_path (str): Full path of the new file
        
    Returns:
        str: The new full path if successful
        
    Raises:
        FileNotFoundError: If the source file does not exist
        FileExistsError: If the destination file already exists
    """
    if not os.path.exists(current_path):
        raise FileNotFoundError(f"Source file {current_path} does not exist")
    
    if os.path.exists(new_path):
        raise FileExistsError(f"Destination file {new_path} already exists")
    
    os.rename(current_path, new_path)
    return new_path


def copy_file_with_metadata(src_path: str, dst_dir: str) -> None:
    """
    Copy a file to a destination directory while preserving metadata.
    Handles macOS-specific file flag issues.
    
    Args:
        src_path (str): Path to the source file
        dst_dir (str): Destination directory path
        
    Raises:
        FileNotFoundError: If the source file does not exist
        OSError: If there are issues during the copy operation
    """
    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"Source file '{src_path}' does not exist")

    filename = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, filename)

    try:
        # First try simple file copy without metadata
        shutil.copy(src_path, dst_path)
        
        # Then try to copy metadata separately, ignoring flag-related errors
        try:
            # Copy file stats (timestamps etc)
            src_stat = os.stat(src_path)
            os.utime(dst_path, (src_stat.st_atime, src_stat.st_mtime))
            
            # Copy permissions
            os.chmod(dst_path, src_stat.st_mode)
        except OSError:
            # Ignore metadata copying errors
            pass
            
    except Exception as e:
        if os.path.exists(dst_path):
            try:
                os.remove(dst_path)
            except:
                pass
        raise OSError(f"Error copying file: {e}")


def generate_new_filename(file_path: str, bin_hash: str, version_number: int) -> str:
    """
    Generate a new filename with version number and hash.
    
    Args:
        file_path (str): Full path or filename containing version number and hash
        bin_hash (str): Binary SHA-256 hash, will be converted to hex_hash to put in filename
        version_number (int): Version number to include in filename
        
    Returns:
        str: Updated filename with version and hash (no path included)
        
    Raises:
        ValueError: If the filename format is invalid for version numbers > 1
    """
    # Convert binary hash to hex
    hex_hash = bin_hash.encode('utf-8').hex()
    
    try:
        base_name = os.path.basename(file_path)

        # Handle version 1 files
        if version_number == 1:
            name, ext = os.path.splitext(base_name)
            return f"{name}-v1-{hex_hash}{ext}"

        # Handle existing versioned files
        pattern = r'(.*-v)(\d+)(-[a-f0-9]{64})(\..*)?$'
        match = re.match(pattern, base_name)
        
        if not match:
            raise ValueError(f"Invalid filename format for versioned file: {base_name}")
        
        prefix = match.group(1)      # Everything up to the version number
        extension = match.group(4) or ''  # File extension (including dot) or empty string
        
        return f"{prefix}{version_number}-{hex_hash}{extension}"
        
    except Exception as e:
        print(f"Error generating new filename for {file_path}: {e}")
        raise