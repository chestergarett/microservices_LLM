from flask import Flask, request, jsonify
import redis
import numpy as np
from redis.commands.search.query import Query
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition
import ast 

app = Flask(__name__)

# Connect to Redis Stack
r = redis.Redis(host='redis', port=6379, decode_responses=False)

VECTOR_DIM = 384  # all-MiniLM-L6-v2
INDEX_NAME = "doc_index"
DOC_PREFIX = "doc:"

def create_vector_index():
    try:
        r.ft(INDEX_NAME).create_index([
            VectorField("embeddings",
                        "FLAT", {
                            "TYPE": "FLOAT32",
                            "DIM": VECTOR_DIM,
                            "DISTANCE_METRIC": "COSINE"
                        }),
            TextField("text")
        ], definition=IndexDefinition(prefix=[DOC_PREFIX]))
    except Exception as e:
        print("Vector DB Error:", e)

@app.route('/add', methods=['POST'])
def add_vector():
    data = request.json
    if isinstance(data['embedding'], str):
        embedding = ast.literal_eval(data['embedding'])
    else:
        embedding = data['embedding']

    vector = np.array(embedding, dtype=np.float32).tobytes()
    key = f"{DOC_PREFIX}{data['id']}"
    r.hset(key, mapping={
        "embedding": vector,
        "text": data['text']
    })
    return jsonify({"status": "stored", "id": data['id']})

@app.route('/search', methods=['POST'])
def search_vector():
    query_vector = np.array(request.json['embedding'], dtype=np.float32).tobytes()

    q = Query(f'*=>[KNN 3 @embeddings $vec_param AS score]') \
        .return_fields("text", "score") \
        .sort_by("score") \
        .dialect(2)

    params = {
        "vec_param": query_vector
    }

    results = r.ft(INDEX_NAME).search(q, query_params=params)

    return jsonify([
        {"text": doc.text, "score": doc.score}
        for doc in results.docs
    ])

@app.route('/flush', methods=['POST'])
def flush_redis():
    try:
        r.flushdb()
        create_vector_index()  # Recreate the index
        return jsonify({"status": "success", "message": "Redis database flushed and index recreated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    create_vector_index()
    app.run(host='0.0.0.0', port=5005)
