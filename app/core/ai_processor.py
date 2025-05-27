from typing import Any, Callable
from app.core.testai import response







MAX_ITERATIONS = 3

def _handle_function_call(conversation: Any, output_item: Any, execute_function: Callable) -> None:
    """Handle a function call from the AI response"""
    conversation.add_function_call(output_item)
    function_result = execute_function(output_item)
    conversation.add_function_result(output_item.call_id, function_result)

def _handle_assistant_message(conversation: Any, output_item: Any, ai_response: Any) -> None:
    """Handle an assistant message from the AI response"""
    conversation.add_assistant_message(output_item)


def process(conversation: Any, execute_function: Callable) -> None:
    """
    Main entry point for AI processing. Takes a conversation and handles:
    - Getting AI response
    - Processing function calls
    - Handling assistant messages
    - Managing follow-up interactions
    """
    ai_response = response(conversation.history)
    
    saw_function_call = False
    saw_assistant_message = False
    follow_up_needed = True
    iterations = 0

    while follow_up_needed and iterations < MAX_ITERATIONS:
        iterations += 1
        
        for output_item in ai_response.output:
            if output_item.type == "function_call":
                saw_function_call = True
                _handle_function_call(conversation, output_item, execute_function)
            elif hasattr(output_item, "role") and output_item.role == "assistant":
                saw_assistant_message = True
                _handle_assistant_message(conversation, output_item, ai_response)

        follow_up_needed = saw_function_call and not saw_assistant_message
        if follow_up_needed:
            ai_response = response(conversation.history)