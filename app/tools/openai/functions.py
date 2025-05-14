from openai import OpenAI
from app.config.settings import OPENAI_API_KEY

def get_transcription(file_path):
    client = OpenAI()
    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    transcription_text = transcript.text
    return transcription_text

def tag_generator_from_description(description):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o-mini",

        instructions="""
        Observe the description provided through the input. Come up
        with up to 8 key word tags that you can attribute to the description based on its content.
        These tags are used to describe a file, and will be used later to find files based on
        things like key people mentioned in the description, places, events, people, activites, etc.
        Exclude any words that dont contribute much meaning to the description.

        Repond with a comma seperated list of these values, no spaces between commas, all lowercase.

        Example description: My family and I are visiting Daii Joons house and
        we went to the nearby resturant and ate together. We also saw Richard on the way there
        while we were on the bus

        Repsonse: "family,resturant,daii joon,richard,bus,

        """,

        input = description
    )

    return response.output_text

