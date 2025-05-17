import time
start_time = time.time()

import os
print(f"os module imported. Time elapsed: {time.time() - start_time:.2f}s")

from typing import Optional, Dict, Any, Tuple
print(f"typing module imported. Time elapsed: {time.time() - start_time:.2f}s")

#FROM OTHER MODULES
from app.tools.openai.functions import get_transcription
print(f"OpenAI module imported. Time elapsed: {time.time() - start_time:.2f}s")

from app.tools.utils import functions as utils
print(f"Utils module imported. Time elapsed: {time.time() - start_time:.2f}s")

from app.tools.mysql.filebase import functions as filebase_functions
print(f"Filebase module imported. Time elapsed: {time.time() - start_time:.2f}s")

from app.tools.mysql.journalbase import functions as journalbase_functions
print(f"Journalbase module imported. Time elapsed: {time.time() - start_time:.2f}s")

class FileData:
    """Class to manage file metadata"""
    def __init__(self):
        self.sha_hash = None
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
        
        self.sha_hash = utils.generate_sha_hash(file_path=file_path,hex_output=False)
        self.size = utils.get_file_size(file_path)
        self.extension = utils.get_file_extension(file_path)

    def determine_version(self, file_path: str) -> None:
        """Determine the version number for the file"""
        # Check if file already exists in database
        if filebase_functions.get_file_id_via_hash(sha_hash=self.sha_hash) != 0:
            raise ValueError("File already exists in the database")
        #Version number will always be one for voice journal uploads
        self.version_number = 1


    def generate_filename(self, file_path: str) -> None:
        """Generate the new filename based on SHA hash, specific to voice recordings"""
        self.name = utils.generate_voicerec_filename(
            file_path=file_path,
            bin_hash=self.sha_hash
        )

    def generate_timestamp(self,file_path:str) -> None:
        """Generate the file timestamp based on its voice rec filename"""
        self.ts = utils.path_to_mysql_datetime(file_path=file_path)

    def to_db_dict(self) -> Dict[str, Any]:
        """Convert object attributes to database-ready dictionary"""
        return {
            key: value for key, value in {
                "sha_hash": self.sha_hash,
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
        file_id = filebase_functions.get_file_id_via_hash(sha_hash=self.sha_hash)
        filebase_functions.insert_file_location(file_id=file_id,location_id=location_id)


def main(file_path):
    print("Generating transcription")
    transcription = get_transcription(file_path=file_path)
    print("Transcription:")
    print(transcription)
    process_choice = input("Press enter to process, press s to skip file: ")
    if process_choice != "":
        return None
    # Initialize and process file data
    file_data = FileData()
    
    # Step 1: Collect initial metadata
    file_data.collect_initial_metadata(file_path=file_path)

    # Step 2: Determine version
    file_data.determine_version(file_path=file_path)

    # Step 3: Determine timestamp from filename
    file_data.generate_timestamp(file_path=file_path)

    # Step 4: Generate new filename
    file_data.generate_filename(file_path)

    # Step 5: Insert into database
    metadata = file_data.to_db_dict()
    filebase_functions.insert_file(file_metadata=metadata)

    # Step 6: Insert location data
    file_data.process_location(location_id=1)

    # Step 7: Insert entry into journalbase
    journalbase_functions.insert_entry(
        entry_text=transcription,
        created_time=file_data.ts,
        file_id=filebase_functions.get_file_id_via_hash(sha_hash=file_data.sha_hash)
    )



