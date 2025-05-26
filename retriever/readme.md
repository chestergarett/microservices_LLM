curl -X POST http://localhost:5003/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?",
    "top_k": 3
  }'
