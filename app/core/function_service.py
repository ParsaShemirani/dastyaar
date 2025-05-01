from typing import Any
import json
from app.tools.registry import function_registry

def execute_function(fragment: Any):
    """
    Execute a function based on the fragment received from the AI response
    """
    function_name = fragment.name
    function_args = json.loads(fragment.arguments)
    function_result = function_registry[function_name](**function_args)
    return function_result