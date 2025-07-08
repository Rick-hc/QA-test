import pandas as pd
from pydantic import BaseModel
from openai import OpenAI
from uuid import uuid4
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db import get_session
from app.models import QA
from app import chroma_client

class Row(BaseModel):
    question: str
    answer: str
    pdf_url: str | None

async def process(path: str):
    df = pd.read_excel(path)
    rows = [Row(**r._asdict()) for r in df.itertuples(index=False)]
    client = OpenAI()
    async for session in get_session():
        for row in rows:
            q_id = str(uuid4())
            emb = client.embeddings.create(model="text-embedding-3-large", input=row.question).data[0].embedding
            await chroma_client.upsert(q_id, row.question, emb)
            await session.execute(
                insert(QA).values(q_id=q_id, question=row.question, answer=row.answer, pdf_url=row.pdf_url)
            )
        await session.commit()

if __name__ == "__main__":
    import sys
    asyncio.run(process(sys.argv[1]))
