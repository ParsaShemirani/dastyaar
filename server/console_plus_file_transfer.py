import code
import io
import contextlib
import os
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import gc
from shutil import rmtree

TRANSFER_DIR = "/home/parsa/transfers"

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



# FILE TRANSFER BELOW



@app.get("/download_file")
def download_file():
    server_file_path = request.args['server_file_path']
    return send_file(server_file_path)

@app.get("/upload_status")
def upload_status():
    filename = request.args['filename']
    folder = os.path.join(TRANSFER_DIR, filename)
    offset_path = os.path.join(folder, "last_offset.txt")

    if not os.path.exists(offset_path):
        return jsonify({"last_offset": None})

    with open(offset_path, 'r') as f:
        hex_offset = f.read().strip()
    return jsonify({"last_offset": hex_offset})

@app.post("/upload_chunk")
def upload_chunk():
    chunk = request.files['chunk']
    file_name = request.form['filename']
    chunk_offset = int(request.form['offset'])

    chunk_hex = f"{chunk_offset:08X}"
    file_folder = os.path.join(TRANSFER_DIR, file_name)
    os.makedirs(file_folder, exist_ok=True)

    chunk_path = os.path.join(file_folder, chunk_hex)
    last_offset_path = os.path.join(file_folder, "last_offset.txt")

    with open(chunk_path, 'wb') as f:
        f.write(chunk.read())

    with open(last_offset_path, 'w') as f:
        f.write(chunk_hex)

    return "OK", 200

@app.post("/assemble_file")
def assemble_file():
    file_name = request.form['filename']
    expected_size = int(request.form['expected_size'])

    folder = os.path.join(TRANSFER_DIR, file_name)
    completed_dir = os.path.join(TRANSFER_DIR, "completed")
    os.makedirs(completed_dir, exist_ok=True)

    def hex_sort_key(filename):
        return int(filename, 16)
    
    all_files = os.listdir(folder)

    chunk_files_list = []
    for f in all_files:
        if not f.endswith(".txt") and len(f) == 8:
            chunk_files_list.append(f)

    chunk_files = sorted(chunk_files_list, key=hex_sort_key)

    total_size = sum(os.path.getsize(os.path.join(folder, f)) for f in chunk_files)
    if total_size != expected_size:
        return f"Size mismatch: got {total_size}, expected {expected_size}", 400

    output_path = os.path.join(completed_dir, file_name)
    with open(output_path, 'wb') as out:
        for chunk_file in chunk_files:
            chunk_path = os.path.join(folder, chunk_file)
            with open(chunk_path, 'rb') as cf:
                out.write(cf.read())
    
    rmtree(folder)

    return "File assembled successfully", 200

"""
Runner script:
gunicorn -w 2 -b 0.0.0.0:8321 --preload server.console:app



Togethermen:
gunicorn -w 2 -b 0.0.0.0:8321 --preload server.console_plus_file_transfer:app

NGROK:
https://2ea6-2601-644-8f00-230-00-d0.ngrok-free.app

LAN:
http://192.168.1.4:8321
KILL ALL GUNICORN:
pkill -f "gunicorn.*server.console:app"
"""