import subprocess
import os


def open_file(filename: str) -> None:
    """
    Open a file using macOS open command.
    
    Args:
        filename (str): The name of the file to open
        
    Returns:
        None
    
    Raises:
        FileNotFoundError: If the file doesn't exist at the specified path
        subprocess.SubprocessError: If the open command fails
    """
    directory = '/Users/parsashemirani/main/firstmacbase'
    file_path = os.path.join(directory, filename)
    
    # Check if file exists before attempting to open
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        subprocess.run(['open', file_path], check=True)
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Failed to open file: {str(e)}")