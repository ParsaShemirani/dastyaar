#These functions seek to deal with the messages context, add new ones, call functions based on response, generate response.

from typing import List, Dict, Any, Tuple, Optional





messages_type = List[Dict[str, Any]]

def messages_appender(
            fragment: Any,
            fragment_kind: str,
            messages: List[messages_type],
            user_input: Optional[str] = None,
            function_output: Optional[Any] = None,
            function_output_id: Optional[str] = None 
) -> messages_type:
    """
    Takes and returns the messages list, 
    
    """

    if fragment_kind == "function_call" and fragment.type == "function_call":
        messages.append({
            "type": "function_call",
            "id": fragment.id,
            "call_id": fragment.call_id,
            "name": fragment.name,
            "arguments": fragment.arguments
        })
    
    elif fragment_kind == "function_call_output":
        messages.append({
            "type": "function_call_output",
            "call_id": function_output_id,
            "output": function_output
        })

    elif fragment_kind == "assistant_message" and fragment.role == "assistant":
        messages.append({
            "id": fragment.id,
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": fragment.content[0].text
                }
            ]
        })
    
    elif fragment_kind == "user_message":
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": user_input
                }
            ]
        })

    return 