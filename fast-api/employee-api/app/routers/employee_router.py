from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.dependencies import EmployeeServiceDep
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=list[EmployeeResponse])
async def list_employees(
    service: EmployeeServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> list[Employee]:
    return service.get_all(skip, limit)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: Annotated[int, Path(ge=1)],
    service: EmployeeServiceDep,
) -> Employee:
    return service.get_by_id(employee_id)


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    data: EmployeeCreate,
    service: EmployeeServiceDep,
) -> Employee:
    return service.create(data)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: Annotated[int, Path(ge=1)],
    data: EmployeeUpdate,
    service: EmployeeServiceDep,
) -> Employee:
    return service.update(employee_id, data)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: Annotated[int, Path(ge=1)],
    service: EmployeeServiceDep,
) -> None:
    service.delete(employee_id)
