from typing import List, Dict, Any, Optional




"""
Creates an instance of "conversation". Does everything related to updating the
conversation, loading old ones. Does not deal with outputting messages
or displaying results, just manages the conversation that the main uses as context
"""



class Conversation:
    def __init__(self,system_prompt:str):
        self.history =[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "No matter what the user says, respond with 'No commands given'"
                    }
                ]
            }
        ]
        self.history[0]["content"][0]["text"] = system_prompt

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



