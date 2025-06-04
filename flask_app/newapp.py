
from flask import Flask,render_template, request, jsonify, redirect

from app.ai_revamp import conversation
from app.core import console
from app.ai_revamp.ai_processor import process

def create_app():
    app = Flask(__name__)

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
            process()
        
        if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            return jsonify({'conversation': conversation.displayconv})
        return render_template('console.html', 
                            historyarr=console.historylist,
                            conversation=conversation.displayconv)
    
    @app.route('/resetconsole', methods=['GET'])
    def resetconsole():
        print(conversation.history)
        console.reset()
        return redirect('/')
    return app