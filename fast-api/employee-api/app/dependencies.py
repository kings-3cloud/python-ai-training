from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db import get_session
from app.repository.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService


def get_employee_repository(
    session: Annotated[Session, Depends(get_session)],
) -> EmployeeRepository:
    return EmployeeRepository(session)


def get_employee_service(
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)],
) -> EmployeeService:
    return EmployeeService(repository)


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
