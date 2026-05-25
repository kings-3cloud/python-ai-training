import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_root(client: AsyncClient):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.headers.get("Content-Type") == "text/plain; charset=utf-8"
    assert resp.text == "That is an ordinary text"

