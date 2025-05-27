import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


from flask import Flask, render_template, jsonify, request, send_file, redirect
from console import CapturingConsole

console = CapturingConsole()



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('console.html', historyarr=console.history)

@app.route('/codeline', methods=['POST'])
def codeline():
    codeline = request.form.get('codeline')
    if codeline is not None:
        console.push(codeline)
    return render_template('console.html', historyarr=console.history)

@app.route('/resetconsole', methods=['GET'])
def resetconsole():
    global console
    console = CapturingConsole() 
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)









if __name__ == '__main__':
    app.run(debug=True)