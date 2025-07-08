from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models import SearchLog

router = APIRouter(prefix="/feedback")

class FeedbackRequest(BaseModel):
    user_query: str
    q1_list: list[str]
    selected_q2: str | None
    topk: int

@router.post("/")
async def feedback(req: FeedbackRequest, session: AsyncSession = Depends(get_session)):
    log = SearchLog(
        user_query=req.user_query,
        candidates=",".join(req.q1_list),
        selected_q2=req.selected_q2,
        topk=req.topk,
    )
    session.add(log)
    await session.commit()
    return {"status": "ok"}
