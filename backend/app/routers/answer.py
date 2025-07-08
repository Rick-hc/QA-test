from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import QA

router = APIRouter(prefix="/answer")

class AnswerRequest(BaseModel):
    q_id: str

class AnswerResponse(BaseModel):
    answer: str
    pdf_url: str | None

@router.post("/", response_model=AnswerResponse)
async def get_answer(req: AnswerRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(QA).where(QA.q_id == req.q_id))
    qa = result.scalar_one_or_none()
    if not qa:
        raise HTTPException(status_code=404, detail="not found")
    return AnswerResponse(answer=qa.answer, pdf_url=qa.pdf_url)
