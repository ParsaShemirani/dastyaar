from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SampleThing:
    file_path: Path
    value1: int
    value2: datetime
    value3: int | None


def insert_thing(sample_thing: SampleThing):
    ...


def create_sample_thing(file_path: Path, value3: int=None):
    if value3:
        sample_thing = SampleThing(
            file_path=file_path,
            value1=1235,
            value2=datetime.now(timezone.utc),
            value3=value3,
        )
    else:
        sample_thing = SampleThing(
            file_path=file_path,
            value1=1235,
            value2=datetime.now(timezone.utc),
        )
    return sample_thing


def insert_sample_thing(file_path: Path, value3: int=None):
    sample_thing = create_sample_thing(
        file_path=file_path,
        value3=value3
    )
    insert_thing(sample_thing=sample_thing)


def add_to_value3(file_path: Path, value3: int=None):
    if value3:
        updated_value3 = value3 + 1
        insert_sample_thing(
            file_path=file_path,
            value3=updated_value3
        )
    else:
        insert_sample_thing(
            file_path=file_path,
            value3=None
        )


def determine_value3(file_path: Path, user_input: str):
    if user_input == "yes":
        value3 = 50
        add_to_value3(file_path=file_path, value3=value3)
    else:
        add_to_value3(file_path=file_path, value3=None)

def make_sample_thing():
    user_input = input("Hello! Would you like to insert value3?")
    file_path = Path(input("Enter a file path"))
    determine_value3(file_path=file_path, user_input=user_input)