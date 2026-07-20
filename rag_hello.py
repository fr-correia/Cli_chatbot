import chromadb
from ollama import embed

client = chromadb.Client()
collection = client.create_collection("test_docs")

docs = [
    "The cli_chatbot project uses uv for dependency management.",
    "MCP standardizes tools, resources, and prompts.",
    "LangGraph uses StateGraph with nodes and edges.",
]

for i, doc in enumerate(docs):
    response = embed(model="nomic-embed-text", input=doc)
    collection.add(
        ids=[str(i)],
        embeddings=response["embeddings"],
        documents=[doc],
    )

query = "How does dependency management work in my project?"
query_embedding = embed(model="nomic-embed-text", input=query)

results = collection.query(
    query_embeddings=query_embedding["embeddings"],
    n_results=1,
)

print(results["documents"])