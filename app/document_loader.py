from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str):
    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path).load()
    else:
        raise ValueError(f"Unsupported file type: {file_path}")