from app.rag import ingest_document, ask
import os
import time

print("Ingesting documents... \n")
docs_dir = "data/documents"
for filename in os.listdir(docs_dir):
    if filename.endswith(".pdf"):
        ingest_document(os.path.join(docs_dir, filename))

questions = [
    "What is the purpose of the code of conduct and who must follow it?",
    "What is the policy on bullying and harassment?",
    "What is the policy on using corporate email?",
    "What are the rules around gifts and entertainment?",
    "What is expected regarding confidential information?",
    "How to access the company network resources?",
    "What are the anti-corruption and bribery rules?",
    "What are the social media guidelines for employees?",
]


print("Answers: \n")
for q in questions:
    print(f"Q: {q}")
    result = ask(q)
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print("-" * 60 + "\n")
    # time.sleep(15)