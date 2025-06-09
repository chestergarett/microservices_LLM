from flask import Flask, request, jsonify
from utils import chunk_pdf_robust, clean_chunk, return_raw_text
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)  # or DEBUG for more verbosity
UPLOAD_FOLDER = "/app/shared_pdfs"  # This matches the mounted Docker volume path

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
    
@app.route('/return_raw_text', methods=['POST'])
def extract_pdf_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        raw_text = return_raw_text(file)

        return jsonify({"raw_text": raw_text}), 200
    except Exception as e:
        app.logger.info(f"Error {str(e)}")
        return jsonify({"Raw Text Error": str(e)}), 500
    
@app.route('/bulk_extract', methods=['GET'])
def bulk_extract_from_mounted_folder():
    folder_path = '/app/shared_pdfs'  # Inside the container
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'rb') as f:
                    raw_text = return_raw_text(f)
                    results.append({
                        'data': {
                            'text': raw_text,
                            'filename': filename
                        }
                    })
            except Exception as e:
                results.append({'filename': filename, 'error': str(e)})

    return jsonify(results), 200

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)
        return jsonify({"message": f"{file.filename} uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
