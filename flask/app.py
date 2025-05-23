import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
from app.tools.mysql.filebase.functions import search_files_description
from app.core.exceptions import DatabaseError

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/filebase')
def filebase():
    return render_template('filebase.html')





@app.route('/filebase/description_search', methods=['POST'])
def filebase_description_search():
    query = request.form.get('query')
    try:
        result = search_files_description(search_text=query)
        return render_template('filebase.html', result=result) 
    except DatabaseError as e:
        return render_template('filebase.html', result=[])



















if __name__ == '__main__':
    app.run(debug=True)