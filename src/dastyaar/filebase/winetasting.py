from dastyaar.filebase.models import File
from datetime import datetime, timezone

def check_adder(file: File):
    file.version_number = 1234123423


james = File(
    root_name="TIMIDBEAST",
    sha256_hash="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    extension="mp3",
    size=234234,
    created_ts=datetime.now(tz=timezone.utc)
)