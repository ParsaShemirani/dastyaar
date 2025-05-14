import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import function from cli programs
from app.cli_programs.file_ingestor.mainrevamp import main as process_file

folder_path = '/Users/parsashemirani/Main/Inbox/jamie'

def main():
    for filename in os.listdir(folder_path):    
        # Build the full path to the file
        file_path = os.path.join(folder_path, filename)
        if filename.startswith('.') or not os.path.isfile(file_path):
            continue  # Skip this file

        print(f"\n=== Processing file: {filename} ===")
        process_file(file_path)  # Pass the file path directly to the main function

if __name__ == "__main__":
    main()