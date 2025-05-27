from flask import Flask, request, jsonify
import numpy as np
import logging
from utils import embed_chunks

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # or DEBUG for more verbosity

@app.route('/embed', methods=['POST'])
def embed():
    data = request.get_json()
    if not data or 'chunks' not in data:
        app.logger.error(f"400 Error: Missing 'chunks' in JSON body, {data}")

        return jsonify({"error": "Missing 'chunks' in JSON body"}), 400

    try:
        chunks = data['chunks']
        embeddings = embed_chunks(chunks)

        if len(chunks) != len(embeddings):
            return jsonify({"error": "Mismatch between number of chunks and embeddings"}), 500

        results = [
            {"text": chunk, 
            "embedding": np.array(embedding).astype(float).tolist()
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]

        return jsonify({"results": results}), 200

    except Exception as e:
        app.logger.error(f"Embedding Error: {str(e)}")
        return jsonify({"Embedding Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
