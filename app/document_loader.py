from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import pytesseract
from pdf2image import convert_from_path
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\Library\bin"

def _is_scanned_pdf(file_path: str) -> bool:
    docs = PyPDFLoader(file_path).load()
    text = " ".join(doc.page_content for doc in docs).strip()
    
    if len(text) < 500:
        return True
    
    # Check ratio of real words vs total characters
    # Scanned PDFs often have lots of whitespace/symbols but few real words
    words = [w for w in text.split() if len(w) > 2 and w.isalpha()]
    total_chars = len(text.replace(" ", ""))
    if total_chars == 0:
        return True
    
    word_char_ratio = sum(len(w) for w in words) / total_chars
    return word_char_ratio < 0.5  # less than 50% real word characters = scanned

def _ocr_pdf(file_path: str) -> list[Document]:
    print(f"Scanned PDF detected, running OCR on {os.path.basename(file_path)}...")
    images = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    docs = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        if text.strip():
            docs.append(Document(
                page_content=text,
                metadata={"source": file_path, "page": i + 1}
            ))
    return docs

def load_document(file_path: str) -> list[Document]:
    if file_path.endswith(".pdf"):
        if _is_scanned_pdf(file_path):
            return _ocr_pdf(file_path)
        else:
            return PyPDFLoader(file_path).load()
    elif file_path.endswith(".txt"):
        from langchain_community.document_loaders import TextLoader
        return TextLoader(file_path, encoding="utf-8").load()
    elif file_path.endswith(".docx"):
        from langchain_community.document_loaders import Docx2txtLoader
        return Docx2txtLoader(file_path).load()
    else:
        raise ValueError(f"Unsupported file type: {file_path}")