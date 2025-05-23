import os
from typing import Optional, Dict, Any, Tuple
from app.tools.utils import functions as utils
from app.tools.mysql.filebase import functions as filebase_functions
from app.cli_programs.file_ingestor import time_configurator
from app.cli_programs.file_ingestor import description_recorder
import shutil
import subprocess




class FileData:
    """Class to manage file metadata"""
    def __init__(self,file_path:str):
        self.file_path = file_path
        self.new_file_path = None
        self.hash = None
        self.name = None
        self.ts = None
        self.ts_precision = None
        self.size = None
        self.extension = None
        self.description = None
        self.version_number = None

    def collect_initial_metadata(self) -> None:
        """Collect metadata that can be gathered immediately from the file"""
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist")
        
        self.hash = utils.generate_sha_hash(file_path=self.file_path,hex_output=False)
        self.size = utils.get_file_size(self.file_path)
        self.extension = utils.get_file_extension(self.file_path)

    def determine_version(self) -> None:
        """Determine the version number for the file"""
        # Check if file already exists in database
        if filebase_functions.get_file_id_via_hash(sha_hash=self.hash) != 0:
            raise ValueError("File already exists in the database")
        # Try to get hash from current filename
        filename_hash = utils.extract_hash_from_filename(file_path=self.file_path)
        if filename_hash == None:
            self.version_number = 1
        else:
            self.version_number = filebase_functions.get_version_number_via_hash(hash_value=filename_hash) + 1

    def handle_timestamp(self) -> None:
        """Handle file timestamp, including alternative method and manual override option"""
        # Set initial timestamp based on version, using birthtime calculation for created time
        if self.version_number == 1:
            self.ts = utils.get_created_time(self.file_path,birthtime=True)
        else:
            self.ts = utils.get_modified_time(self.file_path)
        
        print(f"File timestamp gathered (using brithtime for created): {self.ts}")

        # Ask if ctime should be used instead
        if input("Type 'm' to generate timestamp using modified time").lower() == 'm':
            self.ts = utils.get_modified_time(self.file_path)
            print(f"File timestamp gathered (using modified time): {self.ts}")

        # Handle manual timestamp logic
        if input("Type 'm' to manually override gathered timestamp: ").lower() == 'm':
            self.ts, self.ts_precision = time_configurator.new_ts()

    def generate_filename(self) -> None:
        """Generate the new filename based on SHA hash"""
        self.name = utils.generate_new_filename(
            file_path=self.file_path,
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
    
    def process_location(self, location_name: str) -> None:
        file_id = filebase_functions.get_file_id_via_hash(sha_hash=self.hash)
        filebase_functions.insert_file_location(file_id=file_id,location_name=location_name)




    def renamer(self) -> str:
        """Rename the file on the system and update the new_file_path attribute of the file object"""

        # Get the directory of the original file
        directory = os.path.dirname(self.file_path)

        # Create the new file path using self.name as the filename
        self.new_file_path = os.path.join(directory, self.name)
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Source file {self.file_path} does not exist")
        
        if os.path.exists(self.new_file_path):
            raise FileExistsError(f"Destination file {self.new_file_path} already exists")
        # Rename the file located at file_path
        os.rename(src=self.file_path,dst=self.new_file_path)


    def upload_to_firstmacbase(self):
        """Copy the file to the firstmacbase directory on mac"""
        firstmacbase_dir = '/Users/parsashemirani/Main/firstmacbase_test'
        #Make base path and move it there
        base_path = os.path.join(firstmacbase_dir, self.name)
        try:
            # Copy the file with its metadata
            shutil.copy2(self.new_file_path, base_path)

            # Print confirmation message
            print(f"File '{self.new_file_path}' has been copied to '{base_path}' with metadata.")
        except Exception as e:
            print(f"Error: {e}")




    def remover(self) -> str:
        """
        Remove the file from original ingestion location
        """
        if self.new_file_path and os.path.exists(self.new_file_path):
            os.remove(self.new_file_path)
            print(f"File {self.new_file_path} removed")
        elif os.path.exists(self.file_path):
            os.remove(path=self.file_path)
            print(f"File {self.file_path} removed")


    def process_group(self, group_id: int) -> None:
        file_id = filebase_functions.get_file_id_via_hash(sha_hash=self.hash)
        filebase_functions.insert_file_group(file_id=file_id,group_id=group_id)


        


def main(file_path, group_id = None):

    # Initialize and process file data
    file_data = FileData(file_path=file_path)

    # Collect initial metadata
    file_data.collect_initial_metadata()

    # Determine file version and exit program if file exists
    try:
        file_data.determine_version()
    except ValueError as e:
        print(f"File already exists in database. Error: {e}")
        exit()

    # Generate new filename based on determined version number
    file_data.generate_filename()

    # Open the file for user to view on computer
    subprocess.run(['open', file_path])

    # Ask user if file should be ingested
    ingest_user_choice = str(input("Press enter to ingest the file, any other input to terminate process and delete file"))

    # Process in case file should be deleted and not ingested
    if ingest_user_choice != "":
        file_data.remover()
        exit()

    # Determine timestamp
    file_data.handle_timestamp()

    # Generate filename
    file_data.generate_filename()

    # Ask if user wants to collect description, do so if requested.
    if input("Press enter to provide description, press d otherwise.").lower() != 'd':
        file_data.collect_description()
    
    # Now we have all needed file information, ready to move file and upload data to databases.

    # Upload file to firstmacbase
    file_data.renamer()
    file_data.upload_to_firstmacbase()

    # Remove file from original ingestion location
    file_data.remover()

    # Generate MYSQL metadata and upload to database
    metadata = file_data.to_db_dict()
    filebase_functions.insert_file(file_metadata=metadata)

    # Upload location info for new file (Uploaded to firstmacbase)
    file_data.process_location(location_name='firstmacbase_test')

    #Insert group id information if provided
    if group_id:
        file_data.process_group(group_id=group_id)

    # Process completed!

    print("File ingested successfully")


