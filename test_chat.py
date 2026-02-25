# from app.rag import ingest_document, ask
# import os

# # --- Ingest your PDFs ---
# print("=== Ingesting documents... ===\n")
# docs_dir = "data/documents"
# for filename in os.listdir(docs_dir):
#     if filename.endswith(".pdf"):
#         ingest_document(os.path.join(docs_dir, filename))

# # --- Ask your questions here ---
# questions = [
#     "What are the main rules in the code of conduct?",
#     "What is the policy on using corporate email?",
#     "What are the consequences of violating IT policies?",
#     "What personal use of corporate IT is allowed?",
# ]

# print("\n=== Answers ===\n")
# for q in questions:
#     print(f"Q: {q}")
#     result = ask(q)
#     print(f"A: {result['answer']}")
#     print(f"Sources: {result['sources']}")
#     print("-" * 60 + "\n")

from app.rag import ingest_document, ask
import os
import time

print("=== Ingesting documents... ===\n")
docs_dir = "data/documents"
for filename in os.listdir(docs_dir):
    if filename.endswith(".pdf"):
        ingest_document(os.path.join(docs_dir, filename))

questions = [
    # "What are the main rules in the code of conduct?",
    # "What behavior is expected from employees?",
    # "What is the policy on using corporate email?",
    # "What are the consequences of violating IT policies?",
    # "What personal use of corporate IT is allowed?",
    "What is the company's policy on remote work?",
    "how to access the company network resources?",
]

print("\n=== Answers ===\n")
for q in questions:
    print(f"Q: {q}")
    result = ask(q)
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print("-" * 60 + "\n")
    time.sleep(15)