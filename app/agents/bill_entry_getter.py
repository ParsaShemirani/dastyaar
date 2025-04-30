from openai import OpenAI
from app.tools.mysql.schema import schema_map as mysql_schema
from app.config.settings import OPENAI_API_KEY
# Define this agents function schema using schema.py from the desired module
function_schema = [
    mysql_schema["get_entries"]
]

try:
    client = OpenAI()
    print("OpenAI Connected")
except Exception as e:
    print(f"Failed to create OpenAI client. Message: {e}")



def response(history):
    return client.responses.create(
        model = "gpt-4o-mini",
        input = history,
        text={"format": {"type": "text"}},
        reasoning={},
        tools=function_schema,
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )
