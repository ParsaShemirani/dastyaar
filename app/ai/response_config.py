from openai import OpenAI
from app.tools.settings import OPENAI_API_KEY
from app.ai import conversation

client = OpenAI()

tools = [
    {
    "type": "function",
    "name": "push_code",
    "description": "Execute the given code string in the interactive console and capture the output.",
    "parameters": {
        "type": "object",
        "required": [
        "code_str"
        ],
        "properties": {
        "code_str": {
            "type": "string",
            "description": "The Python code to execute."
        }
        },
        "additionalProperties": False
    },
    "strict": True
    }
]







def response():

    return client.responses.create(
        model = "gpt-4o-mini",
        input = conversation.history,
        reasoning={},
        tools=tools,
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=False
    )