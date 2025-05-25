curl -X POST \
     -H "Content-Type: application/json" \
     -d "{ \"chunks\": [\"This is the first chunk of text.\", \"Here's the second chunk for embedding.\"] }" \
     http://0.0.0.0:5001/embed