from flask import Flask, request, jsonify
from utils import chunk_pdf_robust, clean_chunk
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # or DEBUG for more verbosity

@app.route('/chunk', methods=['POST'])
def chunk():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        chunks = chunk_pdf_robust(file)
        chunks = [clean_chunk(c) for c in chunks]

        return jsonify({"chunks": chunks}), 200
    except Exception as e:
        app.logger.info(f"Error {str(e)}")
        return jsonify({"Chunking Error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
