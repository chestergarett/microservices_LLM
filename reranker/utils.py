from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def rerank_chunks(query, chunks, top_k=5):
    pairs = [(query, chunk) for chunk in chunks]

    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        scores = model(**inputs).logits.squeeze(-1)

    scored_chunks = [
        {"chunk": chunk, "score": float(score)}
        for chunk, score in zip(chunks, scores)
    ]

    ranked = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]
