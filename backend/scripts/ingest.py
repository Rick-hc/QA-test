import argparse
import uuid
import pandas as pd
import asyncio
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import async_session
from app.models import QA
from app.chroma_client import collection
import openai

class Row(BaseModel):
    question: str
    answer: str
    pdf_url: str | None = None

async def upsert_row(row: Row, session: AsyncSession, embed_client):
    q_id = uuid.uuid4()
    qa = QA(q_id=q_id, question=row.question, answer=row.answer, pdf_url=row.pdf_url)
    session.add(qa)
    emb = await embed_client.embeddings.create(
        model="text-embedding-3-large",
        input=row.question,
    )
    collection.upsert(ids=[str(q_id)], embeddings=[emb.data[0].embedding], metadatas=[{"q_id": str(q_id), "question": row.question}])

async def main(path: str):
    df = pd.read_excel(path)
    embed_client = openai.AsyncOpenAI()
    async with async_session() as session:
        for _, r in df.iterrows():
            row = Row(**r.to_dict())
            await upsert_row(row, session, embed_client)
        await session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("excel", help="path to qa.xlsx")
    args = parser.parse_args()
    asyncio.run(main(args.excel))
