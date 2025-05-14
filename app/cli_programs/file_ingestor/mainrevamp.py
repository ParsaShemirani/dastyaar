import os
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

from app.tools.utils import functions as utils
from app.tools.mysql.filebase.functions import FileDBManager
from app.cli_programs.file_ingestor.time_configurator import new_ts
from app.cli_programs.file_ingestor import description_recorder

class FileData:
    """Class to manage file metadata and database operations"""
    def __init__(self):
        self.sha_hash: Optional[bytes] = None
        self.name: Optional[str] = None
        self.ts: Optional[str] = None
        self.ts_precision: Optional[str] = None
        self.size: Optional[int] = None
        self.extension: Optional[str] = None
        self.description: Optional[str] = None
        self.version_number: Optional[int] = None

    def collect_initial_metadata(self, file_path: str) -> None:
        """Collect metadata that can be gathered immediately from the file"""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
        
        self.sha_hash = utils.generate_sha_hash(file_path,False)
        self.size = utils.get_file_size(file_path)
        self.extension = utils.get_file_extension(file_path)

    def determine_version(self, db: FileDBManager, file_path: str) -> None:
        """Determine the version number for the file"""
        # Check if file already exists in database
        if db.check_hash_exists(self.sha_hash):
            raise ValueError("File already exists in the database")

        # Try to get hash from current filename
        filename_hash = utils.extract_hash_from_filename(file_path)
        version_in_base = 0 if filename_hash is None else db.get_version_in_base(filename_hash)
        self.version_number = version_in_base + 1

    def handle_timestamp(self, file_path: str) -> None:
        """Handle file timestamp, including manual override option"""
        # Set initial timestamp based on version
        if self.version_number == 1:
            self.ts = utils.get_created_time(file_path)
        else:
            self.ts = utils.get_modified_time(file_path)

        print(f"File timestamp gathered: {self.ts}")
        if input("Type 'm' to manually override gathered timestamp: ").lower() == 'm':
            self.ts, self.ts_precision = new_ts()

    def generate_filename(self, file_path: str) -> None:
        """Generate the new filename based on SHA hash"""
        hex_sha_hash = utils.generate_sha_hash(file_path,True)
        self.name = utils.generate_new_filename(
            file_path,
            hex_sha_hash,
            self.version_number
        )

    def collect_description(self) -> None:
        """Collect file description using audio recording"""
        self.description = description_recorder.main()

    def to_db_dict(self) -> Dict[str, Any]:
        """Convert object attributes to database-ready dictionary"""
        return {
            "sha_hash": self.sha_hash,
            "name": self.name,
            "ts": self.ts,
            "ts_precision": self.ts_precision,
            "size": self.size,
            "extension": self.extension,
            "description": self.description,
            "version_number": self.version_number
        }

def main(file_path=None):
    try:
        # Initialize database connection
        db = FileDBManager()
        #if not db.check_connection():
          #  raise ConnectionError("Could not connect to database")
        print("Database connection successful")

        # Get file path if not provided
        if file_path is None:
            file_path = input("Please enter the full path to the file: ").strip()
        
        # Initialize and process file data
        file_data = FileData()
        
        # Step 1: Collect initial metadata
        file_data.collect_initial_metadata(file_path)
        
        # Step 2: Determine version
        file_data.determine_version(db, file_path)
        
        # Step 3: Handle timestamp
        file_data.handle_timestamp(file_path)
        
        # Step 4: Generate new filename
        file_data.generate_filename(file_path)
        
        # Step 5: Collect description
        file_data.collect_description()
        
        # Step 6: Insert into database
        metadata = file_data.to_db_dict()
        db.insert_file(metadata)
        print("Metadata inserted successfully")
        
        # Step 7: Handle tags
        file_id = db.get_file_id(file_data.sha_hash)
        tags = description_recorder.tag_generator_from_description(file_data.description)
        db.add_tags_to_file(file_id, tags)
        print("Tags inserted successfully")

        # Step 8: Insert location data

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())