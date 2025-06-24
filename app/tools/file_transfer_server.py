from flask import Flask, request, send_file
import os
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.get("/download_file")
    def download_file():
        server_file_path = request.args['server_file_path']

        return send_file(server_file_path)

    @app.post("/upload_file")
    def upload_file():
        f = request.files['file']
        server_directory = request.form['server_directory']
        server_file_path = os.path.join(server_directory, f.filename)

        with open(server_file_path, "wb") as out:
            for chunk in f.stream:
                out.write(chunk)
        return ""

    @app.post("/upload_chunk")
    def upload_chunk():
        chunk = request.files['chunk']
        file_name = request.form['filename']
        chunk_number = int(request.form['chunk_number'])
        total_chunks = int(request.form['total_chunks'])
        server_directory = request.form['server_directory']

        parts_directory = os.path.join(server_directory, '.chunks')
        os.makedirs(parts_directory, exist_ok=True)
        chunk.save(os.path.join(parts_directory, f'{file_name}.part{chunk_number}'))

        if len(os.listdir(parts_directory)) == total_chunks:
            with open(os.path.join(server_directory, file_name), 'wb') as out:
                for i in range(total_chunks):
                    with open(os.path.join(parts_directory, f'{file_name}.part{i}'), 'rb') as p:
                        out.write(p.read())
                    os.remove(p.name)
                os.rmdir(parts_directory)
        return ""
    
    return app


