from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://host.docker.internal:11434/api/chat"

@app.route('/llm', methods=['POST'])
def llm_query():
    data = request.get_json()

    if not data or 'messages' not in data:
        return jsonify({'LLM Error': 'Missing "query" in request body'}), 400

    try:
        ollama_response = requests.post(
            OLLAMA_URL,
            json={
                "model": data['model'],
                "messages": data['messages'],
                "stream": False,
                "max_tokens": 200,
                "seed": 1
            }
        )
        ollama_response.raise_for_status()
        return jsonify(ollama_response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'LLM Error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
