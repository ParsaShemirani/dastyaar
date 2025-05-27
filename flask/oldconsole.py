import code
import sys
import io

class CapturingConsole(code.InteractiveConsole):
    """
    An interactive console that captures both input commands and their output.
    Stores the history of interactions for later retrieval.
    """
    def __init__(self, locals=None, filename="<console>"):
        """
        Initialize the capturing console.
        
        Args:
            locals: Dictionary of local variables to use in the console
            filename: Name to use for the console in tracebacks
        """
        super().__init__(locals, filename)
        self.history = []
        
    def push(self, line):
        """
        Execute a line of code and capture both the input and any resulting output.
        
        Args:
            line: A string containing a line of Python code to execute
            
        Returns:
            bool: True if more input is needed for a complete command, False otherwise
        """
        # Store the input line with >>> prefix to indicate a command
        self.history.append(f">>> {line}")
        # Redirect stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = sys.stderr = mystream = io.StringIO()
        try:
            more = super().push(line)
            # Get the output, split into lines, store each
            output = mystream.getvalue()
            if output:
                for out_line in output.splitlines():
                    self.history.append(out_line)
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        return more

    
    def push_code(self, code_input):
        """
        Executes Python code, whether a single line or multiple lines.
        
        This function accepts any code input and processes it appropriately:
        - A single line string is executed directly
        - A multi-line string is split and each line is executed sequentially
        - Empty lines are preserved and executed (important for multi-line statements)
        
        Args:
            code_input: A string containing Python code (single or multiple lines)
        
        """
        # Handle completely empty input
        if not code_input:
            self.push("")
            return
            
        lines = code_input.splitlines()
        for line in lines:
            # Process all lines, including empty ones
            self.push(line)

