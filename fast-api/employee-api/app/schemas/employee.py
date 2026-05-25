from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: str
    position: str
    salary: float
    hire_date: date


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[date] = None
    is_active: Optional[bool] = None


class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: date
    is_active: bool

    model_config = {"from_attributes": True}
