import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Now safely load secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_CALENDAR_CLIENT_ID = os.getenv("GOOGLE_CALENDAR_CLIENT_ID")
GOOGLE_CALENDAR_CLIENT_SECRET = os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET")
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "UTC")  # fallback to UTC if not set

