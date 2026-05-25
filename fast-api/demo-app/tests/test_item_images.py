import pytest
from httpx import AsyncClient

JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 16
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16


async def _create_item(client: AsyncClient, name: str = "Image Item") -> int:
    resp = await client.post("/items", json={"name": name, "price": 1.0, "quantity": 1})
    return resp.json()["id"]


@pytest.mark.anyio
async def test_create_item_image_jpeg(client: AsyncClient):
    item_id = await _create_item(client)
    resp = await client.post(
        f"/items/{item_id}/image",
        files={"file": ("photo.jpg", JPEG_BYTES, "image/jpeg")},
    )
    assert resp.status_code == 201
    assert resp.json()["message"] == "Image created successfully"


@pytest.mark.anyio
async def test_create_item_image_png(client: AsyncClient):
    item_id = await _create_item(client)
    resp = await client.post(
        f"/items/{item_id}/image",
        files={"file": ("photo.png", PNG_BYTES, "image/png")},
    )
    assert resp.status_code == 201


@pytest.mark.anyio
async def test_create_item_image_unsupported_type(client: AsyncClient):
    item_id = await _create_item(client)
    resp = await client.post(
        f"/items/{item_id}/image",
        files={"file": ("doc.txt", b"hello world", "text/plain")},
    )
    assert resp.status_code == 415


@pytest.mark.anyio
async def test_create_item_image_bmp_rejected(client: AsyncClient):
    item_id = await _create_item(client)
    resp = await client.post(
        f"/items/{item_id}/image",
        files={"file": ("photo.bmp", b"BM" + b"\x00" * 20, "image/bmp")},
    )
    assert resp.status_code == 415


@pytest.mark.anyio
async def test_get_item_image(client: AsyncClient):
    item_id = await _create_item(client)
    await client.post(
        f"/items/{item_id}/image",
        files={"file": ("photo.png", PNG_BYTES, "image/png")},
    )
    resp = await client.get(f"/items/{item_id}/image")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert resp.content == PNG_BYTES


@pytest.mark.anyio
async def test_get_item_image_not_found(client: AsyncClient):
    item_id = await _create_item(client)
    resp = await client.get(f"/items/{item_id}/image")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_update_item_image(client: AsyncClient):
    item_id = await _create_item(client)
    await client.post(
        f"/items/{item_id}/image",
        files={"file": ("original.jpg", JPEG_BYTES, "image/jpeg")},
    )

    updated_bytes = b"\xff\xd8\xff\xe0" + b"\x01" * 16
    resp = await client.put(
        f"/items/{item_id}/image",
        files={"file": ("updated.jpg", updated_bytes, "image/jpeg")},
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "Image updated successfully"

    get_resp = await client.get(f"/items/{item_id}/image")
    assert get_resp.content == updated_bytes


@pytest.mark.anyio
async def test_update_item_image_changes_content_type(client: AsyncClient):
    item_id = await _create_item(client)
    await client.post(
        f"/items/{item_id}/image",
        files={"file": ("original.jpg", JPEG_BYTES, "image/jpeg")},
    )
    resp = await client.put(
        f"/items/{item_id}/image",
        files={"file": ("new.png", PNG_BYTES, "image/png")},
    )
    assert resp.status_code == 200
    get_resp = await client.get(f"/items/{item_id}/image")
    assert get_resp.headers["content-type"] == "image/png"


@pytest.mark.anyio
async def test_update_item_image_not_found(client: AsyncClient):
    item_id = await _create_item(client)
    resp = await client.put(
        f"/items/{item_id}/image",
        files={"file": ("photo.jpg", JPEG_BYTES, "image/jpeg")},
    )
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_update_item_image_unsupported_type(client: AsyncClient):
    item_id = await _create_item(client)
    await client.post(
        f"/items/{item_id}/image",
        files={"file": ("original.jpg", JPEG_BYTES, "image/jpeg")},
    )
    resp = await client.put(
        f"/items/{item_id}/image",
        files={"file": ("bad.bmp", b"BM" + b"\x00" * 20, "image/bmp")},
    )
    assert resp.status_code == 415
