from pdf2image import convert_from_bytes
import pytesseract
from PyPDF2 import PdfReader
import io
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def extract_text_combined(file):
    file_bytes = file.read()
    images = convert_from_bytes(file_bytes)
    reader = PdfReader(io.BytesIO(file_bytes))

    full_text = ""
    for idx, page in enumerate(reader.pages):
        # Extract text using PyPDF2
        text = page.extract_text() or ""
        # OCR the corresponding image of the page
        ocr_text = pytesseract.image_to_string(images[idx])
        # Combine both
        combined = text.strip() + "\n" + ocr_text.strip()
        full_text += combined + "\n\n"
    return full_text
def clean_chunk(text):
    # Replace smart quotes with standard ones
    text = text.replace('“', '"').replace('”', '"').replace("’", "'")

    # Remove all non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Drop special characters, keeping only alphanumeric and spaces
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)

    # Normalize whitespace (multiple spaces → single space)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def chunk_pdf_robust(file, chunk_size=500, chunk_overlap=50):
    file.seek(0)
    raw_text = extract_text_combined(file)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    return splitter.split_text(raw_text)

