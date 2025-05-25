import redis
import json
from sentence_transformers import SentenceTransformer
import numpy as np

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_INDEX_NAME = "doc_chunks"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def retrieve_similar_chunks(query, top_k=5):
    query_vector = model.encode(query).astype(np.float32).tolist()

    base_query = {
        "vector": query_vector,
        "topK": top_k,
        "includeMetadata": True
    }

    # Use Redis FT search (if Redis is set up with vector similarity indexing)
    res = r.ft(REDIS_INDEX_NAME).search(f"*=>[KNN {top_k} @embedding $vec_param]",
        query_params={"vec_param": json.dumps(query_vector)},
        return_fields=["chunk", "score"],
        dialect=2
    )

    results = []
    for doc in res.docs:
        results.append({
            "chunk": doc.chunk,
            "score": float(doc.score)
        })

    return results
