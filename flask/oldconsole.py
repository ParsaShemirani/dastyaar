"""
Interactive Python console simulator that captures code execution and output.

This module provides a Console class that simulates a Python REPL environment,
capturing both the input code and its output. It handles multi-line code blocks
and maintains a history of all interactions.
"""

import code
import io
import contextlib
from typing import List, Tuple


class Console:
    """
    A class that simulates an interactive Python console/REPL.
    
    This class uses Python's InteractiveConsole to execute code and captures
    both stdin and stdout to provide a complete record of the interaction.
    
    Attributes:
        console (code.InteractiveConsole): The Python interactive interpreter instance.
        historystr (str): A string containing the complete history of inputs and outputs.
        historylist (List[str]): A list storing individual code snippets and their outputs.
        _buffer (List[str]): Internal buffer to track multi-line code entries.
    """
    
    def __init__(self) -> None:
        """
        Initialize a new Console instance with an empty history and buffer.
        """
        self.console = code.InteractiveConsole()
        self.historystr = ""
        self.historylist = []  # List to store individual code snippets
        self._buffer = []  # Internal buffer to track multi-line code
        
    def push_code(self, code_str: str) -> str:
        """
        Execute the given code string in the interactive console and capture the output.
        
        This method processes code as if it were typed into a Python REPL, including
        handling multi-line code blocks and capturing all output (both stdout and stderr).
        
        Args:
            code_str (str): The Python code to execute.
            
        Returns:
            str: A formatted string containing the code with REPL prompts and output.
        
        """
        # Prepare for new output
        snippet = ""
        lines = code_str.splitlines() or [""]
        need_more = False

        # Split code into lines for REPL-style handling
        for i, line in enumerate(lines):
            # Use the appropriate prompt based on whether we're in a code block
            prompt = ">>> " if not need_more else "... "
            snippet += f"{prompt}{line}\n"

            # Capture stdout and stderr during code execution
            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                need_more = self.console.push(line)
                output = buf.getvalue()

            # Only add output if code block completed and there's actual output
            if not need_more and output:
                snippet += output

        # Final blank line to finish code block if necessary
        if need_more:
            prompt = "... "
            snippet += f"{prompt}\n"
            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                self.console.push("")  # Empty string to signal end of input
                output = buf.getvalue()
            if output:
                snippet += output

        # Append to history string
        self.historystr += snippet
        
        # Append each line as a separate element to historylist
        for line in snippet.splitlines():
            if line.strip():  # Skip empty lines
                self.historylist.append(line)
                
        return snippet.rstrip('\n')

# Example usage
if __name__ == "__main__":
    """
    Demonstrates the usage of the Console class.
    
    Executes several code examples to show how the console works,
    including simple print statements and multi-line code blocks.
    """
    # Create a new console instance
    c = Console()
    
    # Example 1: Simple print statement
    print(c.push_code("print('hello world')"))
    print('-'*20)
    
    # Example 2: Multi-line code block (for loop)
    print(c.push_code("for i in range(2):\n    print(i)"))
    print('-'*20)
    
    # Display the complete history
    print("History so far:\n", c.historystr)
