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
        response = client.audio.transcriptions.create(
            file=audio_file,
            **kwargs
        )
    return response

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
    return result





"""
from server.openai_base import generate_response as gr
    
r = gr(
    instructions="Generate a roughly 6 thousand word response for the user which gives guidance and explanation on the topics he seeks information on.",
    model="gpt-4.1",
    temperature=0.2,
    max_output_tokens=30000,
    input=referando
)

"""






"""
args = {
    "instructions": "Generate a two thousand word text of what the user describes",
    "model": "gpt-4.1",
    "temperature": 0.2,
    "max_output_tokens": 3500,
    "input": "So regarding JavaScript at the moment, I have worked with a few examples of just printing basic things to the console and making one API call, but I haven't worked with it much. Before getting into it, I want to get a big picture look at JavaScript, the language. What I don't want is to get too heavy into syntax rules and things like that. I want a bigger picture of the philosophy behind the language, how things are structured, what are distinct characteristics of it, and what I don't want to look into much at the moment either is highly abstracted things like frameworks, but rather I want to be educated more on the roots of JavaScript itself. I don't really want any examples either of code using JavaScript. I want to mainly get the conceptual overview of the language. I'm somewhat familiar with Python and I've used it a lot and written a lot of code in it for my project. I'm used to the flow of things in Python and the way things are normally set up, but I wonder if beyond just the basic syntax differences, if there are more core fundamental differences in the languages and the philosophy behind it. I know the basic things like how it can be run on a server or web browser where Python can be run in a terminal and differences like that, but I'm more wanting to understand and get a feel for what is this language, why should I approach it as a tool for my project. When I approach the tool, what does it look like, what does it feel like, what's unique about it, what do I always see from it. I don't want a text that only teaches me about one aspect of JavaScript, but I want this text that tells me more about the JavaScript and characteristics of it that are apparent anywhere that the language is used. I want to get that sense of knowing and the sense of familiarity of the conceptual level and fundamental level of the language of JavaScript before researching more into it with specific code examples."
}

"""





"""
from server.openai_base import generate_response
args = {
"input": "Give a brief summary of what ai fine tuning is.",
"model": "gpt-4.1",
"temperature": 0
}


mastermind = '''
```
You are given a single debit-card transaction string. Your task is to output exactly one of three labels—`user`, `dad`, or `unsure`—and then a one-sentence explanation.

Rules for labeling:
1. If the merchant or purchase clearly falls under “food” (restaurants, cafes, fast-food), “groceries” (supermarkets, grocery stores), or “transportation” (gas stations, ride-share, public transit), or is a clearly essential household necessity (medicines, toiletries, basic utilities), label `dad`.
2. If the merchant or purchase is clearly non-essential (outdoor gear, entertainment, apparel, electronics, hobbies, gifts, travel unrelated to daily commute), label `user`.
3. If you cannot determine from the merchant name alone whether it's essential or non'essential, label `unsure`.

Output format (with no extra text):
<label>
<explanation>

Example:
Input: “PURCHASE AUTHORIZED ON 05/05 REI #143 DUBLIN DUBLIN CA S585125639378192 CARD 8632”
Output:
```

user
This is a purchase at REI (outdoor gear retailer), which is non-essential, so you pay.

```
```

Use exact matching of merchant names and keywords to decide; do not invent new categories. If merchant name is not on your essential list and not obviously non-essential, choose `unsure`.

'''




args = {
    "model": "gpt-4.1",
    "temperature": 1.3,
    "instructions": prompt,
    "input": "PURCHASE AUTHORIZED ON 05/28 YOGURTLAND CA153 DUBLIN CA S385148691263116 CARD 8632"
}

"""



"""
Generate an image of a man that is skydiving. He is skydiving while simultaneously riding a motorcycle. His parachute is out, he is super high in the air, and he is saddled on the motorcyle which is a sports bike with very race like styling. It is a bright day with the sun out, and you can see the landscape from high up. While he is seated on the motorcycle with the parachute, he is about to drop a large computer from his hand. He is holding the computer in his and and has just let it go, it is bearly past his hand and still close to the motorcycle, he is drop testing it to see if it will survive the fall. He is holding a book in the other hand while he is doing this. 
"""


"""
args = {
    "instructions": "Generate a series of Javascript code examples based on the concept described from the input. Your output text should include the javascript code, some comments within it, and brief sections of explenation between the code sections that describe the mechanics of what the code is doing, and how it relates to the concept at hand. Regarding the character of the examples, they should not be full javascript programs, rather sections of one that are charactaristic of the concept at hand. The examples you generate should give the user, who is new to javascript, insight into how the code looks like, how it achives the certain conceptual tasks. Less emphasis on describing syntactic elements, but rather put emphasis on giving code examples that clearly demonstrate the concept. Your output should be around 600 words total. ",
    "model": "gpt-4.1",
    "temperature": 0.2,
    "max_output_tokens": 3500,
    "input": '''Concept: While it can run virtually anywhere now, JavaScript's soul is still tied to the browser. It's intrinsically tied to the Document Object Model (DOM) and the browser's security model: sandboxed, event-driven, manipulating and reacting to dynamic content. This orientation toward user interfaces and interaction colors the way many programs are written: in JavaScript, you often think in terms of "events," "listeners," and "handlers," rather than simply writing code that does something and quits.'''
}

"""
