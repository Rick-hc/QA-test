from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from openai import AsyncOpenAI

from ..db import get_session
from ..models import QA
from .. import chroma_client

router = APIRouter(prefix="/search")

class SearchRequest(BaseModel):
    candidates: List[str]
    threshold: float = 0.7

class SearchHit(BaseModel):
    q_id: str
    score: float

class SearchResponse(BaseModel):
    hits: List[SearchHit]

@router.post("/", response_model=SearchResponse)
async def search(req: SearchRequest, session=Depends(get_session)):
    client = AsyncOpenAI()
    hits = []
    for cand in req.candidates:
        emb = (await client.embeddings.create(model="text-embedding-3-large", input=cand)).data[0].embedding
        result = chroma_client.query(emb, n_results=5)
        for i, score in zip(result["ids"][0], result["distances"][0]):
            if score >= req.threshold:
                hits.append(SearchHit(q_id=i, score=score))
    hits.sort(key=lambda x: x.score, reverse=True)
    return SearchResponse(hits=hits)
