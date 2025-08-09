from os import getenv
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

filebase_path = getenv("filebase_path")

intake_path = Path("/Users/parsashemirani/Main/fakeintest")


OPENAI_API_KEY = getenv("OPENAI_API_KEY")