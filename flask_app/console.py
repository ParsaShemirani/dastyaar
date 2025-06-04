# Interactive console simulator capturing code execution and output
import code
import io
import contextlib


class Console:
    # Simulate a Python REPL environment and record all interactions
    def __init__(self) -> None:
        self.console = code.InteractiveConsole()
        self.historylist = []  # Interaction history
        self._buffer = []  # Buffer for multi-line inputs

    def push_code(self, code_str: str) -> str:
        # Execute a block of code as if entered in a REPL and capture its output
        snippet = ""
        code_output = ""
        lines = code_str.splitlines() or [""]
        need_more = False

        for i, line in enumerate(lines):
            # Choose primary or continuation prompt based on state
            prompt = ">>> " if not need_more else "... "
            snippet += f"{prompt}{line}\n"

            # Redirect stdout and stderr to capture any output or errors
            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                need_more = self.console.push(line)
                output = buf.getvalue()

            # If this was a complete statement and produced output, record it
            if not need_more and output:
                snippet += output
                code_output += output

        if need_more:
            # Close off any pending multi-line statement
            prompt = "... "
            snippet += f"{prompt}\n"
            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                self.console.push("")  # Close multi-line block
                output = buf.getvalue()
            if output:
                snippet += output
                code_output += output

        # Append each non-blank line of the interaction to history
        for line in snippet.splitlines():
            if line.strip():
                self.historylist.append(line)

        return code_output.rstrip('\n')
