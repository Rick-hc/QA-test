from fastapi import APIRouter
from pydantic import BaseModel
from openai import AsyncOpenAI
from typing import List

router = APIRouter(prefix="/query")

class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    candidates: List[str]

SYSTEM_PROMPT = "You are a helpful assistant that generates search query candidates in Japanese." 

@router.post("/", response_model=QueryResponse)
async def create_candidates(req: QueryRequest):
    client = AsyncOpenAI()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": req.user_query},
    ]
    resp = await client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    text = resp.choices[0].message.content.strip()
    candidates = [line for line in text.splitlines() if line]
    return QueryResponse(candidates=candidates)
