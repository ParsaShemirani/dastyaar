from dastyaar.filebase.models import File
from dastyaar.filebase.novingest import base_ingest
from datetime import datetime, timezone
from pathlib import Path

james = base_ingest(
    file_path=Path('/Users/parsashemirani/Main/fakeactive/advancedo3advice'),
    created_ts=datetime.now(tz=timezone.utc)
)