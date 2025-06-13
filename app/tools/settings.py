import os
from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MYSQL_HOST=os.getenv("MYSQL_HOST")
MYSQL_USER=os.getenv("MYSQL_USER")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")

GOOGLE_MAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")

FILEBASE_FILE = "/Users/parsashemirani/Main/dastyaar/app/tools/filebase_test.db"

AUDIO_OUTPUT_DIRECTORY = "/Users/parsashemirani/Main/dastyaar/"