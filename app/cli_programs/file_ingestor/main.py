import os
from typing import Optional, Dict, Any, Tuple
from app.tools.utils import functions as utils
from app.tools.mysql.filebase import functions as filebase_functions
from app.cli_programs.file_ingestor.time_configurator import new_ts
from app.cli_programs.file_ingestor import description_recorder







class FileData:
    """Class to manage file metadata"""
    def __init__(self):
        self.hash = None
        self.name = None
        self.ts = None
        self.ts_precision = None
        self.size = None
        self.extension = None
        self.description = None
        self.version_number = None

    def collect_initial_metadata(self, file_path: str) -> None:
        """Collect metadata that can be gathered immediately from the file"""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
        
        self.hash = utils.generate_sha_hash(file_path=file_path,hex_output=False)
        self.size = utils.get_file_size(file_path)
        self.extension = utils.get_file_extension(file_path)

    def determine_version(self, file_path: str) -> None:
        """Determine the version number for the file"""
        # Check if file already exists in database
        if filebase_functions.get_file_id_via_hash(sha_hash=self.hash) != 0:
            raise ValueError("File already exists in the database")
        # Try to get hash from current filename
        filename_hash = utils.extract_hash_from_filename(file_path=file_path)
        if filename_hash == None:
            self.version_number = 1
        else:
            self.version_number = filebase_functions.get_version_number_via_hash(hash_value=filename_hash) + 1

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
        self.name = utils.generate_new_filename(
            file_path=file_path,
            bin_hash=self.hash,
            version_number=self.version_number
        )

    def collect_description(self) -> None:
        """Collect file description using audio recording"""
        self.description = description_recorder.main()

    def to_db_dict(self) -> Dict[str, Any]:
        """Convert object attributes to database-ready dictionary"""
        return {
            key: value for key, value in {
                "hash": self.hash,
                "name": self.name,
                "ts": self.ts,
                "ts_precision": self.ts_precision,
                "size": self.size,
                "extension": self.extension,
                "description": self.description,
                "version_number": self.version_number
            }.items() if value is not None
        }
    
    def process_location(self, location_id: int) -> None:
        file_id = filebase_functions.get_file_id_via_hash(sha_hash=self.hash)
        filebase_functions.insert_file_location(file_id=file_id,location_id=location_id)

file_path = 'james'

def main(file_path):

    # Initialize and process file data
    file_data = FileData()
    
    # Step 1: Collect initial metadata
    file_data.collect_initial_metadata(file_path)
    
    # Step 2: Determine version
    file_data.determine_version(file_path)
    
    # Step 3: Handle timestamp
    file_data.handle_timestamp(file_path)
    
    # Step 4: Generate new filename
    file_data.generate_filename(file_path)
    
    # Step 5: Collect description
    file_data.collect_description()

    # Step 6: Insert into database
    metadata = file_data.to_db_dict()
    filebase_functions.insert_file(file_metadata=metadata)

    # Step 8: Insert location data
    file_data.process_location(location_id=1)
