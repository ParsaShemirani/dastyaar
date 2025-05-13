import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now we can import from our app package
from app.cli_programs.voice_recording_uploader.voice_recording_upload import process_file

def main():
    # Example usage
    file_path = '/Users/parsashemirani/Library/Mobile Documents/iCloud~com~dayananetworks~voicerecordpro/Documents/20250513-132822.m4a'
    result = process_file(file_path)
    print(result)

if __name__ == "__main__":
    main()