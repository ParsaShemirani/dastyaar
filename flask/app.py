import os
import sys
import json
from typing import List, Dict, Any, Optional
from console import Console
# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from flask import Flask, render_template, jsonify, request, redirect
from app.core.ai_processor import process
from app.core.conversation import Conversation

app = Flask(__name__)


console = Console()
conversation = Conversation()

def execute_function(tool_call: Any):
    """
    Execute a function based on the call recieved and return the output
    """
    args = json.loads(tool_call.arguments)
    function_output = console.push_code(args["code_str"])
    return function_output





@app.route('/')
def home():
    return render_template('console.html', 
                         historyarr=console.historylist,
                         conversation=conversation.displayconv)

@app.route('/codeline', methods=['POST'])
def codeline():
    codeline = request.form.get('codeline', '').strip()
    if codeline:
        console.push_code(codeline)
    
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        return jsonify({'history': console.historylist})
    return render_template('console.html', historyarr=console.historylist)

@app.route('/input_message', methods=['POST'])
def input_message():
    input_message = request.form.get('input_message', '').strip()
    if input_message:
        conversation.add_user_message(input_message)
        process(conversation=conversation, execute_function=execute_function)
    
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        return jsonify({'conversation': conversation.displayconv})
    return render_template('console.html', 
                         historyarr=console.historylist,
                         conversation=conversation.displayconv)

@app.route('/resetconsole', methods=['GET'])
def resetconsole():
    print(conversation.history)
    global console
    console = Console()
    return redirect('/')












if __name__ == '__main__':
    app.run(debug=True)