from app.tools.audio_recording import interactive_transcribe
from app.tools import read_filebase
from app.tools import write_filebase

def make_new_grouping(name, description):
    write_filebase.create_grouping(
        name=name
    )
    grouping_id = read_filebase.get_last_grouping_id()
    write_filebase.associate_gdescription(
        grouping_id=grouping_id,
        description=description
    )
    result = read_filebase.get_grouping_info_via_id(
        id=grouping_id
    )
    return result










def interactive_mng():
    grouping_name = input("Please type the grouping name: ")

    print("Please describe the grouping\n\n")
    grouping_description = interactive_transcribe()

    result = make_new_grouping(
        name=grouping_name,
        description=grouping_description
    )

    print(result)

"""
from app.tools.groupings_functions import interactive_mng as imng
imng()
"""