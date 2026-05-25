import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_list_items_empty(client: AsyncClient):
    resp = await client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_create_item(client: AsyncClient):
    payload = {"name": "Widget", "description": "A test widget", "price": 9.99, "quantity": 5}
    resp = await client.post("/items", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Widget"
    assert data["description"] == "A test widget"
    assert data["price"] == 9.99
    assert data["quantity"] == 5
    assert data["id"] is not None


@pytest.mark.anyio
async def test_create_item_no_description(client: AsyncClient):
    payload = {"name": "Minimal", "price": 1.0, "quantity": 0}
    resp = await client.post("/items", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Minimal"
    assert data["description"] is None


@pytest.mark.anyio
async def test_create_item_missing_required_fields(client: AsyncClient):
    resp = await client.post("/items", json={"description": "no name or price"})
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_items_returns_all(client: AsyncClient):
    await client.post("/items", json={"name": "Alpha", "price": 1.0, "quantity": 1})
    await client.post("/items", json={"name": "Beta", "price": 2.0, "quantity": 2})
    resp = await client.get("/items")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.anyio
async def test_list_items_limit(client: AsyncClient):
    for i in range(5):
        await client.post("/items", json={"name": f"Item{i}", "price": float(i + 1), "quantity": i})
    resp = await client.get("/items?limit=3")
    assert resp.status_code == 200
    assert len(resp.json()) == 3


@pytest.mark.anyio
async def test_list_items_skip(client: AsyncClient):
    for i in range(5):
        await client.post("/items", json={"name": f"Item{i}", "price": float(i + 1), "quantity": i})
    resp = await client.get("/items?limit=10&skip=3")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.anyio
async def test_list_items_invalid_limit_too_low(client: AsyncClient):
    resp = await client.get("/items?limit=0")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_items_invalid_limit_too_high(client: AsyncClient):
    resp = await client.get("/items?limit=101")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_items_invalid_skip_negative(client: AsyncClient):
    resp = await client.get("/items?skip=-1")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_update_item(client: AsyncClient):
    create_resp = await client.post("/items", json={"name": "Old Name", "price": 1.0, "quantity": 1})
    item_id = create_resp.json()["id"]

    update_payload = {"name": "New Name", "description": "Updated desc", "price": 19.99, "quantity": 10}
    resp = await client.put(f"/items/{item_id}", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == item_id
    assert data["name"] == "New Name"
    assert data["description"] == "Updated desc"
    assert data["price"] == 19.99
    assert data["quantity"] == 10


@pytest.mark.anyio
async def test_update_item_not_found(client: AsyncClient):
    payload = {"name": "Ghost", "price": 1.0, "quantity": 0}
    resp = await client.put("/items/9999", json=payload)
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_update_item_invalid_id(client: AsyncClient):
    payload = {"name": "Bad ID", "price": 1.0, "quantity": 0}
    resp = await client.put("/items/0", json=payload)
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_delete_item(client: AsyncClient):
    create_resp = await client.post("/items", json={"name": "ToDelete", "price": 5.0, "quantity": 1})
    item_id = create_resp.json()["id"]

    resp = await client.delete(f"/items/{item_id}")
    assert resp.status_code == 204

    list_resp = await client.get("/items")
    ids = [item["id"] for item in list_resp.json()]
    assert item_id not in ids


@pytest.mark.anyio
async def test_delete_item_not_found(client: AsyncClient):
    resp = await client.delete("/items/9999")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_delete_item_invalid_id(client: AsyncClient):
    resp = await client.delete("/items/0")
    assert resp.status_code == 422
