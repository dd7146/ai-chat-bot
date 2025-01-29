import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            template_folder=os.path.abspath('../frontend/templates'),
            static_folder=os.path.abspath('../frontend/static'))

CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.abspath('../frontend/static'), path)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data['message']

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({
            'response': response.choices[0].message['content']
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Print paths for verification (optional)
    print("Template path:", os.path.abspath('../frontend/templates'))
    print("Static path:", os.path.abspath('../frontend/static'))
    app.run(debug=True)