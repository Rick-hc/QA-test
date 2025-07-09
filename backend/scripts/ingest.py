# backend/scripts/ingest.py
import os
import argparse
import uuid
import pandas as pd
import asyncio
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
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
    collection.upsert(
        ids=[str(q_id)],
        embeddings=[emb.data[0].embedding],
        metadatas=[{"q_id": str(q_id), "question": row.question}],
    )

async def main(paths: list[str]):
    embed_client = openai.AsyncOpenAI()
    async with async_session() as session:
        for path in paths:
            df = pd.read_excel(path, engine="openpyxl")
            for _, r in df.iterrows():
                row = Row(**r.to_dict())
                await upsert_row(row, session, embed_client)
        await session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="複数の Excel ファイル（ローカルパス or URL）を読み込み、QA と Embedding を登録"
    )
    # 複数可に変更
    parser.add_argument(
        "excels",
        nargs="*",
        help="読み込む Excel ファイルのパスまたは URL（複数可）"
    )
    args = parser.parse_args()

    # ■① コマンド引数があればそれを使い、なければ環境変数 QA_EXCEL_URLS を読む
    paths = args.excels or os.getenv("QA_EXCEL_URLS", "").split(",")
    # ■② 空エントリを除去
    paths = [p.strip() for p in paths if p.strip()]

    if not paths:
        raise SystemExit("エクセルのパス or URL を引数 or 環境変数 QA_EXCEL_URLS で指定してください")

    # ■③ リストを main() に渡す
    asyncio.run(main(paths))
