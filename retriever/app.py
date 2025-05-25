from flask import Flask, request, jsonify
from utils import retrieve_similar_chunks

app = Flask(__name__)

@app.route('/retrieve', methods=['POST'])
def retrieve():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in JSON body"}), 400

    try:
        results = retrieve_similar_chunks(data['query'], top_k=data.get("top_k", 5))
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
