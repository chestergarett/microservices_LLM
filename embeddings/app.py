from flask import Flask, request, jsonify
from utils import embed_chunks

app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def embed():
    data = request.get_json()
    if not data or 'chunks' not in data:
        return jsonify({"error": "Missing 'chunks' in JSON body"}), 400

    try:
        chunks = data['chunks']
        embeddings = embed_chunks(chunks)

        if len(chunks) != len(embeddings):
            return jsonify({"error": "Mismatch between number of chunks and embeddings"}), 500

        results = [
            {"text": chunk, "embedding": embedding}
            for chunk, embedding in zip(chunks, embeddings)
        ]

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
