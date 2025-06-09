FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install system-level dependencies required for spaCy and training
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libz-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && python -m spacy validate

# Link the model if it exists
RUN python -m spacy link /app/custom_ner_model custom_ner_model || true

EXPOSE 5015
CMD ["python", "app.py"]
