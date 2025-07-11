# app/chroma_client.py
import os
import chromadb
from urllib.parse import urlparse
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

raw = os.getenv("CHROMA_HOST", "http://chroma:8000")
parts = urlparse(raw)

client = chromadb.HttpClient(
    host=parts.hostname or "chroma",
    port=parts.port or 8000,
    ssl=parts.scheme == "https",
)

# Default collection used across the application. It attaches an embedding
# function so that queries can be issued with plain text.
embedder = OpenAIEmbeddingFunction(
    model_name="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY"),
)

collection = client.get_or_create_collection(
    "default", embedding_function=embedder
)
