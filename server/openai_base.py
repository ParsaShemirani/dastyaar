from openai import OpenAI
import base64
from server.settings import OPENAI_API_KEY

def generate_response(**kwargs):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        **kwargs
    )
    return response

def generate_transcription(audio_file_path, **kwargs):
    client = OpenAI(api_key=OPENAI_API_KEY)

    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            **kwargs
        )
    transcription_text = transcript.text
    return transcription_text

def generate_speech_from_text(output_audio_file_path, **kwargs):
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    with client.audio.speech.with_streaming_response.create(
            **kwargs
    ) as response:
        response.stream_to_file(output_audio_file_path)

def generate_image(output_image_file_path, **kwargs):
    client = OpenAI(api_key=OPENAI_API_KEY)

    result = client.images.generate(
            **kwargs
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(output_image_file_path, "wb") as f:
        f.write(image_bytes)