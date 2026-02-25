import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.document_loader import load_document
from langchain_ollama import ChatOllama

load_dotenv()

VECTORSTORE_PATH = "data/vectorstore"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.2)
llm = ChatOllama(model="llama3.2", temperature=0.2)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def _load_or_create_store():
    if os.path.exists(VECTORSTORE_PATH) and os.listdir(VECTORSTORE_PATH):
        return FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def ingest_document(file_path: str):
    docs = load_document(file_path)
    chunks = splitter.split_documents(docs)
    
    for chunk in chunks:
        chunk.metadata["source"] = file_path

    store = _load_or_create_store()
    if store:
        store.add_documents(chunks)
    else:
        store = FAISS.from_documents(chunks, embeddings)
    os.makedirs(VECTORSTORE_PATH, exist_ok=True)
    store.save_local(VECTORSTORE_PATH)
    print(f"Ingested: {file_path} ({len(chunks)} chunks)")

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful HR assistant. Answer the employee's question using ONLY the context below.
If the answer isn't in the context, say "I don't have that information in the company documents."

Context:
{context}

Question: {question}

Answer:"""
)

def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask(question: str) -> dict:
    store = _load_or_create_store()
    if not store:
        return {"answer": "No documents have been ingested yet.", "sources": []}

    retriever = store.as_retriever(search_kwargs={"k": 4})

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(question)
    source_docs = retriever.invoke(question)
    sources = list({doc.metadata.get("source", "unknown") for doc in source_docs})

    return {"answer": answer, "sources": sources}