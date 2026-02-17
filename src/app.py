# src/app.py
from flask import Flask, request, jsonify, render_template
from gemini_agent import ask_groq
import os

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get response with error handling
    reply = ask_groq(user_input)
    
    # Check if it's an error message
    if reply.startswith('❌'):
        return jsonify({
            'response': reply,
            'error': True,
            'suggestion': 'Wait 1 minute or check API key'
        }), 200  # Return 200 but show error in UI
    
    return jsonify({'response': reply, 'error': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)