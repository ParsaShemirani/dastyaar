from dastyaar.filebase.way_new_ingest import create_first_version_file, create_new_version_file_and_edge, create_file_description_and_edge
from pathlib import Path
from datetime import datetime, timezone
from dastyaar.filebase.connection import Session
path = Path('/Users/parsashemirani/Main/Inbox/junkers/flask_logbase_website/app.py')

'''
with Session() as session:
    with session.begin():
        buzit, mozeet = create_new_version_file_and_edge(file_path=path, session=session)
        buzit.created_ts = datetime.now(timezone.utc)
        session.add_all([buzit, mozeet])
    session.refresh(buzit)
    session.refresh(mozeet)
'''


with Session() as session:
    with session.begin():
        moz = create_first_version_file(file_path=path, session=session)
        moz.created_ts = datetime.now(timezone.utc)
        monkey = [moz]
        monkey.extend(create_file_description_and_edge(file=moz, description_text="TIMIX TMUX JAMES"))

        session.add_all(monkey)