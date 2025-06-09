from flask import Flask, request, jsonify
from utils import predict
import spacy

trained_nlp = spacy.load('custom_ner_model')
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    entities = predict(text,trained_nlp)
    return jsonify(entities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)