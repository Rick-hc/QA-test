import chromadb
from chromadb.api.types import Documents, Embedding

client = chromadb.HttpClient(host="chroma", port=8000)
collection = client.get_or_create_collection("default")

async def upsert(q_id: str, question: str, embedding: Embedding):
    collection.upsert(documents=[question], ids=[q_id], embeddings=[embedding], metadatas=[{"q_id": q_id, "question": question}])

def query(embedding: Embedding, n_results: int = 5):
    return collection.query(query_embeddings=[embedding], n_results=n_results)
