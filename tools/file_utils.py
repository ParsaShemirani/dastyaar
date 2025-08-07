from pathlib import Path
from hashlib import file_digest
from re import match, search

def generate_sha256_hash(file_path: Path) -> str:
    with file_path.open('rb') as f:
        return file_digest(f, "sha256").hexdigest()

def extract_rootname_from_path(file_path: Path) -> str:
    pass




file_name_regex = r"^(?P<root_name>.+)-v(?P<version_number>\d+)-(?P<sha256_hash>[0-9a-fA-F]{64})(?:\.(?P<extension>.+))$"

sha256_hash_regex = r"[0-9a-fA-F]{64}"

sample_file_name = "sample_file_cool-v123-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.mp3"

jmatch = match(pattern=file_name_regex, string=sample_file_name)

print(jmatch.group('version_number'))

print(type(jmatch.group('version_number')))



print("MONEY TIME")

james = Path('/Users/parsashemirani/Main/Inbox/moneynoext')

tomato = james.suffix

print(tomato)
print(type(tomato))


newj = tomato.lstrip('.')

print("THE NEW ERa")

print(newj)