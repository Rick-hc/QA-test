from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter(prefix="/query", tags=["query"])

class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    candidates: list[str]

@router.post("", response_model=QueryResponse)
async def generate_candidates(req: QueryRequest):
    prompt = (
        "ユーザーの質問を改善するため、関連しそうな候補質問を5つまで日本語で箇条書きで出力してください: "
        f"{req.user_query}"
    )
    chat = await openai.AsyncOpenAI().chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    text = chat.choices[0].message.content
    candidates = [line.strip("- ") for line in text.splitlines() if line.strip()]
    return QueryResponse(candidates=candidates)
