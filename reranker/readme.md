curl -X POST http://localhost:5003/rerank \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?",
    "chunks": [
      "Paris is the capital and most populous city of France.",
      "Berlin is the capital of Germany.",
      "Madrid is the capital of Spain."
    ],
    "top_k": 2
  }'
