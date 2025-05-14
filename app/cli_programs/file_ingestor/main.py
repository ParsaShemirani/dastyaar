
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

#FROM OTHER MODULES
from app.tools.utils import functions as utils
from app.tools.mysql.filebase.functions import FileDBManager
from time_configurator import new_ts


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
        self.ts = "NONE" #MEEANT TO UPDATE
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
    file_data = SQLFileData()
    file_data.get_file_metadata(file_path)

    #Try to get the hash from the current filename. If there is no hash,
    #that means it has not been in the base before.
    #If there is a hash, we will get the version number from the database.
    file_db = FileDBManager()
    filename_hash = utils.extract_hash_from_filename(file_path)
    if filename_hash is None:
        version_in_base = 0
    else:
        try:
            version_in_base = file_db.get_version_in_base(filename_hash)
        except Exception as e:
            print(f"Error retrieving version from database: {e}")
            exit()

    file_data.version_number = version_in_base + 1

    if version_in_base == 0:
        file_data.ts = utils.get_created_time(file_path)
    else:
        file_data.ts = utils.get_modified_time(file_path)
    
    man_ts = input("Type m to manually override gathered ts: ")

    if man_ts != "":
        file_data.ts, file_data.ts_precision = new_ts()
    
    hexa_sha_hash_current = utils.generate_sha_hash(file_path,True)
    file_data.name = utils.generate_new_filename(file_path, hexa_sha_hash_current, version_in_base)   

    file_db.insert_file(file_data.to_db_dict())
    file_id = file_db.get_file_id(file_data.sha_hash)
    if file_id:
        #Insert the file_id along with storage location 1 for file_location table
        file_db.insert_location(file_id,1)

