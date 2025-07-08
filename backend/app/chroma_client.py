import os
import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "http://localhost:8000")

client = chromadb.HttpClient(host=CHROMA_HOST.replace("http://", ""))
collection = client.get_or_create_collection("default")
