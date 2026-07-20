from pathlib import Path
import chromadb
from ollama import embed, chat

DB_PATH = "rag/chroma_store"
SOURCE_FILE = "README.md"  # point this at any real text file in your project

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("project_docs")

def index_file(path: str):
    text = Path(path).read_text(encoding="utf-8")
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    for i, chunk in enumerate(chunks):
        response = embed(model="nomic-embed-text", input=chunk)
        collection.upsert(
            ids=[f"{path}-{i}"],
            embeddings=response["embeddings"],
            documents=[chunk],
        )
    print(f"indexed {len(chunks)} chunks from {path}")

def answer(query: str, n_results: int = 3) -> str:
    query_embedding = embed(model="nomic-embed-text", input=query)
    results = collection.query(
        query_embeddings=query_embedding["embeddings"],
        n_results=n_results,
    )
    context = "\n\n".join(results["documents"][0])

    messages = [
        {"role": "system", "content": "Answer using only the provided context. If the context doesn't contain the answer, say so."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
    ]
    response = chat(model="qwen3:8b", messages=messages, think=False)
    return response.message.content

if __name__ == "__main__":
    index_file(SOURCE_FILE)
    print(answer("What does this project do?"))