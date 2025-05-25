from sentence_transformers import SentenceTransformer

# Load model once globally
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks):
    embeddings = model.encode(chunks, convert_to_numpy=True).tolist()
    return embeddings
