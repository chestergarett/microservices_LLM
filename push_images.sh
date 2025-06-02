#!/bin/bash

# Define your Docker Hub username
DOCKER_HUB_USER=chestergarett

# List of services to build and push
services=("chunker" "embeddings" "reranker" "retriever" "vector_db" "llm", "scraper")

for service in "${services[@]}"; do
    echo "🚧 Building and pushing image for $service..."

    docker buildx build \
        --platform linux/amd64 \
        -t $DOCKER_HUB_USER/$service:latest \
        ./$service \
        --push

done

echo "✅ All images built and pushed successfully!"
