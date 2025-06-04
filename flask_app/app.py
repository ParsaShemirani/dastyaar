import os
import sys
import json
from flask import Flask, render_template, jsonify, request, redirect
from flask_app.console import Console
from app.core.ai_processor import process
from app.core.conversation import Conversation
def create_app():

    app = Flask(__name__)

    # Store objects as app attributes
    app.console = Console()
    app.conversation = Conversation()

    def execute_function(tool_call):
        args = json.loads(tool_call.arguments)
        function_output = app.console.push_code(args["code_str"])
        return function_output

    @app.route('/')
    def home():
        return render_template('console.html', 
                            historyarr=app.console.historylist,
                            conversation=app.conversation.displayconv)

    @app.route('/codeline', methods=['POST'])
    def codeline():
        codeline = request.form.get('codeline', '').strip()
        if codeline:
            app.console.push_code(codeline)
        
        if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            return jsonify({'history': app.console.historylist})
        return render_template('console.html', historyarr=app.console.historylist)

    @app.route('/input_message', methods=['POST'])
    def input_message():
        input_message = request.form.get('input_message', '').strip()
        if input_message:
            app.conversation.add_user_message(input_message)
            process(conversation=app.conversation, execute_function=execute_function)
        
        if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            return jsonify({'conversation': app.conversation.displayconv})
        return render_template('console.html', 
                            historyarr=app.console.historylist,
                            conversation=app.conversation.displayconv)

    @app.route('/resetconsole', methods=['GET'])
    def resetconsole():
        print(app.conversation.history)
        app.console = Console()
        return redirect('/')

    return app
