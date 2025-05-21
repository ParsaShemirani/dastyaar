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





@app.route('filebase/description_search', methods=['POST'])
def filebase_description_search():
    query = request.form.get('query')
    try:
        result = search_files_description(search_text=query)
        return render_template('filebase', result = (result))
    except DatabaseError as e:
        return None



















if __name__ == '__main__':
    app.run(debug=True)