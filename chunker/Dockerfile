FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for pdf2image (poppler-utils) and Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

EXPOSE 5004

CMD ["python", "app.py"]
