from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SampleThing:
    file_path: Path
    value1: int
    value2: datetime
    value3: int | None
    

def create_sample_thing(file_path: Path):
    sample_thing = SampleThing(
        file_path=file_path,
        value1=1235,
        value2=datetime.now(timezone.utc),
    )
    return sample_thing


def insert_thing(sample_thing: SampleThing):
    ...


def add_to_value_3(value3):
    updated_value3 = value3 + 1
    return value3

def make_sample_thing():
    user_input = input("Hello! Would you like to insert value3?")
    file_path = Path(input("Enter a file path"))
    sample_thing = create_sample_thing(file_path=file_path)

    if user_input == "yes":
        value3 = 50
        updated_value3 = add_to_value_3(value3=value3)
        sample_thing.value3 = updated_value3
    
    insert_thing(sample_thing=sample_thing)