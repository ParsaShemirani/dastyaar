from pathlib import Path
from hashlib import file_digest

def generate_sha256_hash(file_path: Path) -> str:
    with file_path.open('rb') as f:
        return file_digest(f, "sha256").hexdigest()

def extract_rootname_from_path(file_path: Path) -> str:
    pass




regex = r"^(?P<root_name>.+)-v(?P<version_number>\d+)-(?P<sha256_hash>.{64})(?:\.(?P<extension>.+))$"

