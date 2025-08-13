from pathlib import Path
import shutil
from dastyaar.settings import intake_storage_device_path
file_path = Path('/Users/parsashemirani/Main/Inbox/junkers/flask_logbase_website/describeddb.txt')

new_file_path = file_path.with_name("TIMMYJONES.md")
file_path.rename(new_file_path)
print(new_file_path)
print("GUZMONEY\n\n\n\n")
print(str(intake_storage_device_path / new_file_path.name))
shutil.move(src=str(new_file_path), dst=intake_storage_device_path) 