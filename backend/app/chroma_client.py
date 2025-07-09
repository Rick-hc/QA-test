# app/chroma_client.py
import os
import chromadb
from urllib.parse import urlparse

raw = os.getenv("CHROMA_HOST", "http://chroma:8000")
parts = urlparse(raw)

client = chromadb.HttpClient(
    host=parts.hostname or "chroma",
    port=parts.port or 8000,
    ssl=parts.scheme == "https",
)
