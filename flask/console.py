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
    
    def push_multiline(self, code_str):
        """
        Executes multiple lines of Python code by breaking the string
        into individual lines and calling push() on each line.
        
        Args:
            code_str: A string containing multiple lines of Python code
        """
        lines = code_str.splitlines()
        for line in lines:
            self.push(line)

