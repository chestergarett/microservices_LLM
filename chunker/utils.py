from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text
    return full_text

def chunk_pdf_with_textsplitter(file, chunk_size=500, chunk_overlap=50):
    raw_text = extract_text_from_pdf(file)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    chunks = splitter.split_text(raw_text)
    return chunks
