import pytest
from httpx import AsyncClient

BASE_URL = "/employees"

VALID_EMPLOYEE = {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "salary": 75000.0,
    "hire_date": "2022-03-15",
}


async def _create_employee(client: AsyncClient, overrides: dict = {}) -> dict:
    payload = {**VALID_EMPLOYEE, **overrides}
    resp = await client.post(BASE_URL, json=payload)
    assert resp.status_code == 201
    return resp.json()


# ---------------------------------------------------------------------------
# GET /employees
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_list_employees_empty(client: AsyncClient):
    resp = await client.get(BASE_URL)
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_list_employees_returns_created(client: AsyncClient):
    await _create_employee(client)
    await _create_employee(client, {"email": "other@example.com"})
    resp = await client.get(BASE_URL)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.anyio
async def test_list_employees_limit(client: AsyncClient):
    for i in range(5):
        await _create_employee(client, {"email": f"user{i}@example.com"})
    resp = await client.get(f"{BASE_URL}?limit=3")
    assert resp.status_code == 200
    assert len(resp.json()) == 3


@pytest.mark.anyio
async def test_list_employees_skip(client: AsyncClient):
    for i in range(5):
        await _create_employee(client, {"email": f"user{i}@example.com"})
    resp = await client.get(f"{BASE_URL}?skip=3&limit=10")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.anyio
async def test_list_employees_invalid_limit(client: AsyncClient):
    resp = await client.get(f"{BASE_URL}?limit=0")
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# GET /employees/{id}
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_get_employee(client: AsyncClient):
    created = await _create_employee(client)
    resp = await client.get(f"{BASE_URL}/{created['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == VALID_EMPLOYEE["email"]
    assert data["first_name"] == VALID_EMPLOYEE["first_name"]


@pytest.mark.anyio
async def test_get_employee_not_found(client: AsyncClient):
    resp = await client.get(f"{BASE_URL}/9999")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_get_employee_invalid_id(client: AsyncClient):
    resp = await client.get(f"{BASE_URL}/0")
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /employees
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_create_employee(client: AsyncClient):
    resp = await client.post(BASE_URL, json=VALID_EMPLOYEE)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] is not None
    assert data["first_name"] == "Jane"
    assert data["email"] == "jane.smith@example.com"
    assert data["is_active"] is True


@pytest.mark.anyio
async def test_create_employee_duplicate_email(client: AsyncClient):
    await _create_employee(client)
    resp = await client.post(BASE_URL, json=VALID_EMPLOYEE)
    assert resp.status_code == 400
    assert "already exists" in resp.json()["detail"]


@pytest.mark.anyio
async def test_create_employee_negative_salary(client: AsyncClient):
    payload = {**VALID_EMPLOYEE, "salary": -1000.0}
    resp = await client.post(BASE_URL, json=payload)
    assert resp.status_code == 400
    assert "Salary" in resp.json()["detail"]


@pytest.mark.anyio
async def test_create_employee_zero_salary(client: AsyncClient):
    payload = {**VALID_EMPLOYEE, "salary": 0.0}
    resp = await client.post(BASE_URL, json=payload)
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_create_employee_future_hire_date(client: AsyncClient):
    payload = {**VALID_EMPLOYEE, "hire_date": "2099-01-01"}
    resp = await client.post(BASE_URL, json=payload)
    assert resp.status_code == 400
    assert "Hire date" in resp.json()["detail"]


@pytest.mark.anyio
async def test_create_employee_invalid_email(client: AsyncClient):
    payload = {**VALID_EMPLOYEE, "email": "not-an-email"}
    resp = await client.post(BASE_URL, json=payload)
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_create_employee_missing_required_fields(client: AsyncClient):
    resp = await client.post(BASE_URL, json={"first_name": "Only"})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# PUT /employees/{id}
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_update_employee(client: AsyncClient):
    created = await _create_employee(client)
    resp = await client.put(
        f"{BASE_URL}/{created['id']}",
        json={"position": "Senior Engineer", "salary": 90000.0},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["position"] == "Senior Engineer"
    assert data["salary"] == 90000.0
    assert data["first_name"] == "Jane"  # unchanged


@pytest.mark.anyio
async def test_update_employee_deactivate(client: AsyncClient):
    created = await _create_employee(client)
    resp = await client.put(
        f"{BASE_URL}/{created['id']}",
        json={"is_active": False},
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False


@pytest.mark.anyio
async def test_update_employee_duplicate_email(client: AsyncClient):
    first = await _create_employee(client)
    second = await _create_employee(client, {"email": "second@example.com"})
    resp = await client.put(
        f"{BASE_URL}/{second['id']}",
        json={"email": first["email"]},
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_update_employee_negative_salary(client: AsyncClient):
    created = await _create_employee(client)
    resp = await client.put(
        f"{BASE_URL}/{created['id']}",
        json={"salary": -500.0},
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_update_employee_not_found(client: AsyncClient):
    resp = await client.put(f"{BASE_URL}/9999", json={"position": "Ghost"})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /employees/{id}
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_delete_employee(client: AsyncClient):
    created = await _create_employee(client)
    resp = await client.delete(f"{BASE_URL}/{created['id']}")
    assert resp.status_code == 204

    get_resp = await client.get(f"{BASE_URL}/{created['id']}")
    assert get_resp.status_code == 404


@pytest.mark.anyio
async def test_delete_employee_not_found(client: AsyncClient):
    resp = await client.delete(f"{BASE_URL}/9999")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_delete_employee_invalid_id(client: AsyncClient):
    resp = await client.delete(f"{BASE_URL}/0")
    assert resp.status_code == 422
