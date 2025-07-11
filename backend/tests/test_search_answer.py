import types
import pytest

from app.routers import search as search_module, answer as answer_module

class DummyEmbedResult:
    def __init__(self):
        self.data = [types.SimpleNamespace(embedding=[0.1, 0.2])]

class DummyEmbedClient:
    async def create(self, model, input):
        return DummyEmbedResult()

class DummyOpenAI:
    def __init__(self):
        self.embeddings = DummyEmbedClient()

class DummyCollection:
    def query(self, query_embeddings, n_results):
        return {
            "ids": [["123"]],
            "distances": [[0.1]],
            "metadatas": [[{"question": "dummy"}]]
        }

class DummySession:
    async def execute(self, q):
        class R:
            def scalar_one_or_none(self_inner):
                return types.SimpleNamespace(answer="ans", pdf_url="url")
        return R()

async def dummy_get_session():
    yield DummySession()

@pytest.mark.asyncio
async def test_search_embeds_and_returns_hits(client, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(search_module, "collection", DummyCollection())
    monkeypatch.setattr(search_module, "openai", types.SimpleNamespace(AsyncOpenAI=lambda: DummyOpenAI()))
    resp = await client.post("/search", json={"candidates": ["foo"], "threshold": 0, "topk": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"][0]["q_id"] == "123"

@pytest.mark.asyncio
async def test_answer_returns_record(client, monkeypatch):
    monkeypatch.setattr(answer_module, "get_session", dummy_get_session)
    resp = await client.post("/answer", json={"q_id": "123"})
    assert resp.status_code == 200
    assert resp.json()["answer"] == "ans"
