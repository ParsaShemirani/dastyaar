from datetime import datetime, timezone
from pathlib import Path

from tools.ingestor import ingest_file, ingest_client_file


file = Path('/Users/parsashemirani/Main/Inbox/junkers/themanhunter.txt')


datetime_object = datetime.fromtimestamp(file.stat().st_birthtime, tz=timezone.utc)

tomato = ingest_file(file_path=file, ctime=datetime_object)

#tomato = ingest_client_file(file_path=file, ctime=datetime_object, description="THIS IS A TESTERMAN DESCRIPTION")



