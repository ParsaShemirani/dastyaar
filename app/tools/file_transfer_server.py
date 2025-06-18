from flask import Flask, request, send_file
import os


def create_app():
    app = Flask(__name__)

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
    
    return app


