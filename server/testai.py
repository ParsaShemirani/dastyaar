from openai import OpenAI
from server.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

prompt = """
Whatever you type, it will be executed on python REPL. Use this to help the user and his request. Nothing you respond with directly reaches the user, only the code you send will be executed. Use the provided examples and guides as reference to what you have access to.
You will also be provided a current history of the REPL to know where you are starting from. Everything you respond with will be entered in the REPL

**REFERENCE**

Opening a file for the user:
example user request: " I want you to open the picture of my dad at his birthday party"
Instructions:
We must first let the user know we will work on it, then find the file in the database, and retrieve its name. Then we will use the open_file
function to open it to the user, then let the user know that it has been opened.

example python:
>>> from app.tools.sqlite_read_functions import match_fdescription
>>> from app.tools.utils import open_file
>>> from app.tools.communication import user_message

>>> user_message("Alright, I am working on finding and opening the picture for you.")
>>> result = match_fdescription("the picture of my dad at his birthday party")
>>> print(result)
{'name': "dad_pic2021", "id": 123}
>>> open_file(result['name'])
>>> user_message("I have opened the picture for you")

**END OF REFERENCE**



CURRENT USER REQUEST: Please open the video of my sister and I at central park

**CURRENT REPL**
>>>
**END OF CURRENT REPL**
"""

jamesprompt = """
Whatever you type, it will be executed on python REPL. Use this to help the user and his request. Nothing you respond with directly reaches the user, only the code you send will be executed. Use the provided examples and guides as reference to what you have access to.
You will also be provided a current history of the REPL to know where you are starting from. Also, regarding newlines: dont actually type the newline character, 
print the backslash followed by n so that it gets interpreted as such by python.


USER MESSAGE: write a binary object that is the world hello but written in binary. make a new file called 'tester.txt'. Make sure that when
you are writing the binary object, you use the b string notation with the backslashes and hexadeciaml values.

"""

def maker():
    response = client.responses.create(
        model='gpt-4o',
        input=jamesprompt
    )
    binaryresponse = response.output_text.encode('utf-8')
    with open('airesponsegaming', 'wb') as f:
        f.write(binaryresponse)
    return response