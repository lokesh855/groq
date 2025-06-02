from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "model": "llama3-70b-8192"  # or try llama3-8b-8192, llama3-70b-8192
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    # Debugging: print response to see what's wrong
    try:
        response_json = response.json()
    except ValueError:
        return jsonify({"reply": "Error: Invalid JSON returned from Groq API."})

    if response.status_code != 200:
        return jsonify({
            "reply": f"Error from Groq API: {response_json.get('error', {}).get('message', 'Unknown error')}"
        })

    try:
        reply = response_json['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except KeyError:
        return jsonify({"reply": f"Unexpected response format: {response_json}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    