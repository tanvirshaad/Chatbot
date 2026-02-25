from app.document_loader import load_document

docs = load_document("data/documents/Itransition Code of Conduct.pdf")
for i, doc in enumerate(docs):
    print(f"--- Page {i+1} ---")
    print(doc.page_content[:300])
    print()