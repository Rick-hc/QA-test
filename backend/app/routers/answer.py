from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_session
from ..models import QA

router = APIRouter(tags=["answer"])  # prefix指定なし

class AnswerRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    pdf_url: str | None

@router.post("/answer", response_model=AnswerResponse)
async def get_answer(req: AnswerRequest, session: AsyncSession = Depends(get_session)):
    # 質問文で検索
    result = await session.execute(select(QA).where(QA.question == req.question))
    qa = result.scalar_one_or_none()
    if not qa:
        raise HTTPException(status_code=404, detail="Not found")
    return AnswerResponse(answer=qa.answer, pdf_url=qa.pdf_url)

# ここは、ユーザーが選択した質問に対する回答を取得するエンドポイントです。
# データベースから質問IDに基づいて回答を取得し、結果を返します。
# もし質問が見つからない場合は、404エラーを返します。また、回答と関連するPDFのURLも返します。