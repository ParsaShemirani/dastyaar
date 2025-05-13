import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

#FROM OTHER MODULES
from app.tools.openai.functions import get_transcription
from app.tools.utils import functions as utils
from app.tools.mysql.filebase.functions import FileDBManager
from app.tools.mysql.journalbase.functions import JournalDBManager


def path_to_mysql_datetime(filepath):
    """
    Given a file path whose basename is in the form
      YYYYMMDD-HHMMSS.ext
    interprets that timestamp in America/Los_Angeles (PST/PDT),
    converts it to UTC, and returns a MySQL DATETIME string.
    """
    # 1) Extract filename and strip extension
    filename = os.path.basename(filepath)
    base_name = filename.split('.')[0]       # e.g. "20250511-203057"
    
    # 2) Split date/time and parse to naive datetime
    date_part, time_part = base_name.split('-')
    dt_naive = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
    
    # 3) Localize to LA time (zoneinfo will handle PST vs PDT)
    la_tz = ZoneInfo("America/Los_Angeles")
    dt_local = dt_naive.replace(tzinfo=la_tz)
    
    # 4) Convert to UTC
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))
    
    # 5) Format for MySQL DATETIME (no timezone suffix)
    return dt_utc.strftime("%Y-%m-%d %H:%M:%S")

class SQLFileData:
    def __init__(self):
        self.sha_hash = None
        self.name = None
        self.ts = None
        self.ts_precision = None
        self.size = None
        self.extension = None
        self.description = None
        self.version_number = None

    def get_file_metadata(self, file_path):
        """Update instance attributes with metadata from the given file."""
        # Assign binary sha_hash to sha_hash attribute
        self.sha_hash = utils.generate_sha_hash(file_path, False)
        # Get hexa sha_hash, make new filename based off of it
        hexa_sha_hash_current = utils.generate_sha_hash(file_path, True)
        self.name = utils.generate_voicerec_filename(file_path, hexa_sha_hash_current)
        # Other attributes
        self.version_number = 1
        self.extension = utils.get_file_extension(file_path)
        self.ts = path_to_mysql_datetime(file_path)
        self.size = utils.get_file_size(file_path)

    def to_db_dict(self) -> dict:
        """Convert the object's attributes to a database-ready dictionary"""
        return {
            'name': self.name,
            'sha_hash': self.sha_hash,
            'ts': self.ts,
            'size': self.size,
            'extension': self.extension,
            'version_number': self.version_number
        }

def process_file(file_path):
    transcription = get_transcription(file_path)
    print("Transcription:")
    print(transcription)
    process_choice = input("Press enter to process, press s to skip file: ")

    if process_choice == "":
        # Initialize database managers
        file_db = FileDBManager()
        journal_db = JournalDBManager()
        
        # Get file metadata
        file_data = SQLFileData()
        file_data.get_file_metadata(file_path)
        
        # Check if file already exists in database
        if file_db.check_hash_exists(file_data.sha_hash):
            print(f"File with hash {file_data.sha_hash} already exists in database")
            return None
            
        # Insert file metadata into database
        if file_db.insert_file(file_data.to_db_dict()):
            # Get the file ID for the journal entry
            file_id = file_db.get_file_id(file_data.sha_hash)
            if file_id:
                #Insert the file_id along with storage location 1 for file_location table
                file_db.insert_location(file_id,1)
                # Insert the transcription as a journal entry
                journal_db.insert_entry(transcription, file_data.ts, file_id)
                print("File and transcription processed successfully")
                return file_data
        
        print("Error processing file")
        return None
    return None
