from server import openai_base

def whisper_transcription(audio_file_path):
    response = openai_base.generate_transcription(
        audio_file_path=audio_file_path,
        model='whisper-1'
    )
    return response.text