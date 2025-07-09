#  このコードはEmbeddingを使用して、ユーザーの質問に関連する候補質問を生成し、選択肢として表示します。
#　また、閾値を設定して、関連性の高い質問のみを表示します。
#  }
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
# ここが検索エンドポイントです。
# ユーザーが選択した候補質問に対して、関連する質問を検索し、結果を返します。    
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
# ここで、ChromaDBを使用して、埋め込みを検索します。
# 埋め込みは、ユーザーの質問と候補質問の関連性を示します。
#　また、ｎ_resultsを5に設定して、最も関連性の高い質問を5つ取得します。
    results = []
    for idx, emb in enumerate(embeddings):
        docs = collection.query(query_embeddings=[emb], n_results=5)
        for q_id, score, meta in zip(docs["ids"][0], docs["distances"][0], docs["metadatas"][0]):
            sim = 1 - score  # chroma returns distance
            if sim >= req.threshold:
                results.append(SearchResult(q_id=q_id, score=sim, question=meta["question"]))
    results.sort(key=lambda x: x.score, reverse=True)
    return SearchResponse(results=results[:5])
