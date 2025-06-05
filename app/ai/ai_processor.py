from typing import Any
from app.ai.response_config import response
from app.core import console
from app.ai import conversation
import json

MAX_ITERATIONS = 6



def _handle_function_call(output_item):
    conversation.add_function_call(function_call=output_item)
    args = json.loads(output_item.arguments)
    function_output = console.push_code(code_str=args['code_str'])
    conversation.add_function_result(call_id=output_item.call_id, result=function_output)

def process() -> None:
    """
    Main entry point for AI processing. Takes a conversation and handles:
    - Getting AI response
    - Processing function calls
    - Handling assistant messages
    - Managing follow-up interactions
    """
    ai_response = response()
    
    follow_up_needed = True
    iterations = 0

    while follow_up_needed and iterations < MAX_ITERATIONS:
        iterations += 1
        print("ITIRATION GAMING")
        print(iterations)
        for output_item in ai_response.output:
            if output_item.type == "function_call":
                saw_function_call = True
                _handle_function_call(output_item=output_item)
            elif hasattr(output_item, "role") and output_item.role == "assistant":
                saw_assistant_message = True
                conversation.add_assistant_message(message=output_item)

        if 'output' in conversation.history[-1]:
            follow_up_needed = True
        else:
            follow_up_needed = False
        if follow_up_needed:
            ai_response = response()