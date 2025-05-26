# microservices_LLM

This repository is a modular, microservice-based Retrieval-Augmented Generation (RAG) framework designed for flexibility, reusability, and easy integration. It enables large language models (LLMs) to generate context-aware responses by retrieving relevant chunks of data from an external source.

## 🧱 Architecture Overview

Each component is isolated into a service to enable scalability, reuse, and clean separation of concerns.

```
                   +-----------+
                   |  Client   |
                   +-----------+
                        |
                        v
                 +-------------+
                 |   LLM API   |  <-- /llm
                 +-------------+
                        |
          ---------------------------------
          |            |                |
          v            v                v
   +----------+   +------------+   +-------------+
   | Retriever|   | Embeddings |   | Reranker    |
   +----------+   +------------+   +-------------+
                        |
                        v
                 +--------------+
                 | Vector Store |
                 +--------------+

```

## 🔌 Microservices

Each folder represents an independent service:

- `llm/`: Interfaces with LLMs like Ollama or OpenAI. Takes user prompts and retrieved context.
- `chunker/`: Splits documents into manageable chunks.
- `retriever/`: Uses vector search to retrieve relevant chunks based on query.
- `embeddings/`: Converts chunks into vector representations using an embedding model.
- `reranker/`: Optionally re-ranks retrieved documents to improve relevance.
- `vector_db/`: Wraps the vector store logic (e.g., FAISS, Qdrant, Chroma).

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Ollama (or any LLM backend running on localhost)
- Python 3.10+ (if running locally)

### Running All Services

```bash
docker-compose up --build
```

Make sure Ollama is running outside the container on your host machine (`http://host.docker.internal:11434`) if LLM is used.

## 🧪 Example Query

```bash
curl -X POST http://localhost:5009/llm \
  -H "Content-Type: application/json" \
  -d '{
        "model": "llama3.2",
        "messages": [{
          "role": "user",
          "content": "Tell me about climate change."
        }]
      }'
```

## 📁 Structure

```
microservices_LLM/
├── chunker/
├── embeddings/
├── llm/
├── retriever/
├── reranker/
├── vector_db/
├── docker-compose.yml
└── README.md
```

## 📌 Notes

- All services expose their own API and can be scaled independently.
- You can plug-and-play with different vector databases or LLMs.
- Stream output support can be added for real-time applications.
