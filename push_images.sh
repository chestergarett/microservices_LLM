#!/bin/bash

# Set your Docker Hub username
DOCKER_HUB_USER="chestergarett"

# List of services to push
services=("chunker" "embeddings" "reranker" "retriever" "vector_db" "llm")

# Build, tag, and push each image
for service in "${services[@]}"; do
    echo "🚧 Building image for $service..."
    docker build -t $DOCKER_HUB_USER/$service:latest ./$service

    echo "🏷️ Tagging image as $DOCKER_HUB_USER/$service:latest"
    docker tag $DOCKER_HUB_USER/$service:latest $DOCKER_HUB_USER/$service:latest

    echo "📤 Pushing $service to Docker Hub..."
    docker push $DOCKER_HUB_USER/$service:latest
done

echo "✅ All images pushed successfully!"
