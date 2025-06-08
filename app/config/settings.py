import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Now safely load secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MYSQL_HOST=os.getenv("MYSQL_HOST")
MYSQL_USER=os.getenv("MYSQL_USER")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")

GOOGLE_MAPS_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")

FILEBASE_FILE = "/Users/parsashemirani/Main/filebase.db"
