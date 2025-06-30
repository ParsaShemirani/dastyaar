import code
import io
import contextlib
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask import after_this_request
import gc

class Console:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.history_string = ""
        self._buffer = []

    def reset(self):
        self.console = code.InteractiveConsole()
        self.history_string = ""
        self._buffer = []
        gc.collect() 

    def push_code(self, code_str):
        snippet = ""
        code_output = ""
        lines = code_str.splitlines() or [""]
        need_more = False

        for i, line in enumerate(lines):
            prompt = ">>> " if not need_more else "... "
            snippet += f"{prompt}{line}\n"

            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                need_more = self.console.push(line)
                output = buf.getvalue()

            if not need_more and output:
                snippet += output
                code_output += output

        if need_more:
            prompt = "... "
            snippet += f"{prompt}\n"
            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                self.console.push("")
                output = buf.getvalue()
            if output:
                snippet += output
                code_output += output

        for line in snippet.splitlines():
            if line.strip():
                self.history_string += line + "\n"

        return code_output.rstrip('\n')
    
    
def replace_92_110_with_10(lst):
    i = 0
    while i < len(lst) - 1:
        if lst[i] == 92 and lst[i + 1] == 110:
            lst[i] = 10
            del lst[i + 1]
        else:
            i += 1
    return lst






app = Flask(__name__)
CORS(app)

console = Console()

@app.post('/console_push')
def console_push():
    binary_code = request.get_data()
    binary_array = list(bytearray(binary_code))
    correct_nl_array = replace_92_110_with_10(lst=binary_array)
    correct_nl_binary = bytes(correct_nl_array)
    correct_nl_decoded = correct_nl_binary.decode('utf-8')
    output_str = console.push_code(code_str=correct_nl_decoded)
    encoded_output = output_str.encode('utf-8')

    return Response(
        response=encoded_output,
        mimetype='application/octet-stream',
        status=200
    )

@app.get('/console_history_string')
def console_history_string():
    binary_string = console.history_string.encode('utf-8')
    return Response(
        response=binary_string,
        mimetype='application/octet-stream',
        status=200
    )

@app.post('/soft_reset')
def soft_reset():
    console.reset()
    return "Soft restarting!", 200

@app.post('/reset_console')
def reset_console():
    import threading
    import time
    
    def delayed_exit():
        time.sleep(0.1)  # Allow response to be sent
        os._exit(0)
    
    threading.Thread(target=delayed_exit).start()
    return "Restarting!", 200



"""
Runner script:
gunicorn -w 1 -b 0.0.0.0:8321 --preload server.console:app

Other:
gunicorn -w 1 -b 127.0.0.1:8321 --preload server.console:app

NGROK:
https://2ea6-2601-644-8f00-230-00-d0.ngrok-free.app

LAN:
http://192.168.1.4:8321
KILL ALL GUNICORN:
pkill -f "gunicorn.*server.console:app"
"""