from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import openai
from ..chroma_client import collection

router = APIRouter(prefix="/search", tags=["search"])

class SearchRequest(BaseModel):
    candidates: List[str]
    threshold: float = 0.8

class SearchResult(BaseModel):
    q_id: str
    score: float
    question: str

class SearchResponse(BaseModel):
    results: List[SearchResult]

@router.post("", response_model=SearchResponse)
async def search(req: SearchRequest):
    embed_client = openai.AsyncOpenAI()
    embeddings = []
    for q in req.candidates:
        emb = await embed_client.embeddings.create(
            model="text-embedding-3-large",
            input=q,
        )
        embeddings.append(emb.data[0].embedding)

    results = []
    for idx, emb in enumerate(embeddings):
        docs = collection.query(query_embeddings=[emb], n_results=5)
        for q_id, score, meta in zip(docs["ids"][0], docs["distances"][0], docs["metadatas"][0]):
            sim = 1 - score  # chroma returns distance
            if sim >= req.threshold:
                results.append(SearchResult(q_id=q_id, score=sim, question=meta["question"]))
    results.sort(key=lambda x: x.score, reverse=True)
    return SearchResponse(results=results[:5])
