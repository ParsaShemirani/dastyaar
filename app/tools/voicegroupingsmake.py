from app.tools.filebase_functions import make_new_grouping
from app.tools.audio_recording import interactive_transcribe
def interactive_mng():
    grouping_name = input("Please type the grouping name: ")

    print("Please describe the grouping\n\n")
    grouping_description = interactive_transcribe()

    result = make_new_grouping(
        grouping_name=grouping_name,
        description=grouping_description
    )

    print(result)

"""
from app.tools.voicegroupingsmake import interactive_mng as imng
imng()
"""