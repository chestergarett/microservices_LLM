import redis
import json
from sentence_transformers import SentenceTransformer
from redis.commands.search.query import Query # Import Query class
import numpy as np

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_INDEX_NAME = "doc_index"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def retrieve_similar_chunks(query, top_k=5):
    import redis
import json
from sentence_transformers import SentenceTransformer
from redis.commands.search.query import Query # Import Query class
import numpy as np

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_INDEX_NAME = "doc_index"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def retrieve_similar_chunks(query, top_k=5):
    print(f"Input query to embed: '{query}'")

    query_embedding_array = model.encode(query, convert_to_numpy=True).astype(np.float32)
    query_vector_bytes = query_embedding_array.tobytes()

    print(f"Shape of query_embedding_array: {query_embedding_array.shape}") # Should be (384,)
    print(f"Size in bytes: {len(query_vector_bytes)}") # Should be 1536

    search_query = (
        # Ensure "@embeddings" matches your VectorField name from index creation
        # 'AS score' aliases the distance to 'score'
        Query(f"*=>[KNN {top_k} @embeddings $vec_param AS score]")
        .sort_by("score") # Sorts by the aliased score
        .return_fields("chunk", "score") # Requests 'chunk' and the aliased 'score'
        .dialect(2)
    )

    params = {"vec_param": query_vector_bytes}

    try:
        res = r.ft(REDIS_INDEX_NAME).search(search_query, query_params=params)
    except Exception as e:
        print(f"Error executing RediSearch query: {e}")
        raise # Re-raise to see the full traceback

    # --- CRUCIAL DEBUGGING PRINTS ---
    print("\n--- RediSearch Raw Response Object ---")
    print(f"Result type: {type(res)}")
    print(f"Total results found: {res.total}")
    if res.docs:
        print(f"First doc object: {res.docs[0]}")
        print(f"Attributes available on first doc (dir()): {dir(res.docs[0])}")
        print(f"Dictionary view of first doc (__dict__): {res.docs[0].__dict__}")
        if hasattr(res.docs[0], 'score'):
            print(f"Explicit check: 'score' attribute EXISTS. Value: {res.docs[0].score}")
        else:
            print("Explicit check: 'score' attribute DOES NOT exist on doc object.")
    else:
        print("No documents returned by the search.")
    print("------------------------------------\n")
    # --- END DEBUGGING PRINTS ---

    results = []
    for doc in res.docs:
        results.append({
            "chunk": doc.chunk.decode('utf-8'), # Decode bytes to string
            "score": float(doc.score) # This is the line that caused the error
        })

    return results

