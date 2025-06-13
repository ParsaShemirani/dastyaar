from openai import OpenAI
from app.tools.settings import OPENAI_API_KEY

def get_transcription(file_path):
    client = OpenAI()
    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    transcription_text = transcript.text
    return transcription_text

