import pytest

@pytest.mark.asyncio
async def test_query(client):
    resp = await client.post("/query/", json={"user_query": "test"})
    assert resp.status_code in (200, 401, 429)
