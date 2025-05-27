from flask import Flask, request, jsonify
from utils import rerank_chunks

app = Flask(__name__)

@app.route('/rerank', methods=['POST'])
def rerank():
    data = request.get_json()
    if not data or 'query' not in data or 'chunks' not in data:
        return jsonify({"Reranking Error": "Missing 'query' or 'chunks' in JSON body"}), 400

    try:
        results = rerank_chunks(data['query'], data['chunks'], top_k=data.get("top_k", 5))
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"Reranking Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
    