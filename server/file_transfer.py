from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

TRANSFER_DIR = "/home/parsa/transfers"

def create_app():
    app = Flask(__name__)
    CORS(app)

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

        return "File assembled successfully", 200
    
    return app
