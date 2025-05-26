from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

EMBEDDING_SERVICE_URL = "http://embeddings:5001/embed"
VECTOR_DB_SERVICE_URL = "http://vector_db:5005/search"

@app.route('/retrieve', methods=['POST'])
def retrieve():
    try:
        data = request.get_json()
        print("Received data:", data)
        if 'query' not in data:
            return jsonify({"error": "Missing 'query' in request"}), 400

        # Build embedding request
        embedding_request = {
            "chunks": [data['query']]
        }

        # Request embedding
        print("Sending request to embedding service...")
        try:
            query_response = requests.post(EMBEDDING_SERVICE_URL, json=embedding_request, timeout=10)
            query_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error during embedding request:", e)
            return jsonify({"error": "Embedding service request failed", "details": str(e)}), 500

        # Parse embedding response
        print("Embedding response received.")
        try:
            query_embeddings = query_response.json()
            print("Embedding response JSON:", query_embeddings)
            embedding_vector = query_embeddings["results"][0]["embedding"]
        except (ValueError, KeyError, IndexError) as e:
            print("Error parsing embedding response:", e)
            return jsonify({"error": "Invalid response format from embedding service", "details": str(e)}), 500

        # Prepare vector DB search request
        query_embeddings_request = {"embedding": embedding_vector}
        print("Sending request to vector DB service...")

        try:
            search_results = requests.post(VECTOR_DB_SERVICE_URL, json=query_embeddings_request, timeout=10)
            search_results.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error during vector DB request:", e)
            return jsonify({"error": "Vector DB service request failed", "details": str(e)}), 500

        print("Vector DB response received.")
        print("Status Code:", search_results.status_code)
        print("Raw Response:", search_results.text)

        # Try parsing JSON response from vector DB
        try:
            return jsonify(search_results.json())
        except ValueError as e:
            print("Error decoding JSON from vector DB response:", e)
            return jsonify({"error": "Invalid JSON response from vector DB", "details": str(e)}), 500

    except Exception as e:
        print("Unexpected error in /retrieve route:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
