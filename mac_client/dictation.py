import os
from mac_client import audio_recording
from mac_client.file_transfer import upload_file
from mac_client import console

def dictate():
    input("Press enter to start recording")
    record_again = True
    while record_again == True:
        audio_recording.record()
        audio_recording.convert_to_mp3()
        upload_file(
            local_file_path=audio_recording.mp3_converted,
            server_directory='/home/parsa/temporary'
        )
        transcription = console.push_code(f"""\
from server.openai_general import whisper_transcription as wt
file_path = '/home/parsa/temporary/recorded_output.mp3'
transcription = wt(file_path)
print(transcription)
            
import os
os.remove(file_path)
""")
        print("Transcription: ", transcription)
        choice = input("Press enter to approve, r to record again")
        record_again = False if choice == '' else True
    os.remove(audio_recording.mp3_converted)
    return transcription


"""
from mac_client.dictation import dictate
dictate()
"""