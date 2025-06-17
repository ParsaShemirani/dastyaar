import os
from dotenv import load_dotenv
load_dotenv()
# FOLDERS ALWAYS END WITH TRAILING SLASH

testing_mode = True

if testing_mode:
    TO_INGEST_PATH = '/Users/parsashemirani/Main/to_ingest_test/'
    INGESTED_PATH = '/Users/parsashemirani/Main/ingested_test/'
    INTAKE_DRIVE_PATH = "/mnt/wdhd/test_base/"
    FILEBASE_DB_FILE = "/home/parsa/sqflaskhost/filebase_test.db"
else:
    TO_INGEST_PATH = '/Users/parsashemirani/Main/to_ingest/'
    INGESTED_PATH = '/Users/parsashemirani/Main/ingested/'
    INTAKE_DRIVE_PATH = "/mnt/wdhd/"
    FILEBASE_DB_FILE = "/home/parsa/sqflaskhost/filebase.db"


BONYAAD_COMPUTER_USER = 'parsa'
BONYAAD_COMPUTER_HOST = '192.168.1.4'

AUDIO_OUTPUT_DIRECTORY = "/Users/parsashemirani/Main/dastyaar/"


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GOOGLE_MAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")


FLASK_PORT = 5321

