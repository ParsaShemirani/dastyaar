from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.get("/download_file")
def download_file():
    file_name = request.args['file_name']
    location_path = request.args['location_path']
    path = os.path.join(location_path, file_name)

    return send_file(path)

@app.post("/upload_file")
def upload_file():
    f = request.files['file']
    location_path = request.form['location_path']
    path = os.path.join(location_path, f.filename)

    with open(path, "wb") as out:
        for chunk in f.stream:
            out.write(chunk)
    return ""

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5034)

