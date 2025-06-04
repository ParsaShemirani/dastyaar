"""
Creates an instance of "conversation". Does everything related to updating the
conversation, loading old ones. Does not deal with outputting messages
or displaying results, just manages the conversation that the main uses as context
"""
from typing import List, Dict, Any, Optional


class Conversation:
    def __init__(self):
        import os
        prompt_path = os.path.join(os.path.dirname(__file__), "newprompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            instructions = f.read()

            self.history =[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": instructions
                        }
                    ]
                }
            ]
    
        self.displayconv= []


    def add_user_message(self, text:str) -> None:
        """
        Add a user message to the conversation history
        """
        self.history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": text
                    }
                ]
            }
        )
        self.displayconv.append(f"You: {text}")
    
    def add_assistant_message(self, message: Any) -> None:
        """
        Add an assistant's response to the conversation history
        """

        self.history.append(
            {
                "id": message.id,
                "role": "assistant",
                "content":[
                    {
                        "type": "output_text",
                        "text": message.content[0].text
                    }
                ]
            }
        )
        self.displayconv.append(f"Assistant: {message.content[0].text}")
    
    def add_function_call(self, function_call: Any) -> None:
        """
        Add a function call to the conversation history
        """
        self.history.append(
            {
                "type": "function_call",
                "id": function_call.id,
                "call_id": function_call.call_id,
                "name": function_call.name,
                "arguments": function_call.arguments
            }
        )
    
    def add_function_result(self, call_id: str, result: Any) -> None:
        """
        Add a function result to the conversation history
        """
        self.history.append(
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": repr(result)
            }
        )



