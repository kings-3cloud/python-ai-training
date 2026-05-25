from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    department: str = Field(max_length=100)
    position: str = Field(max_length=100)
    salary: float
    hire_date: date
    is_active: bool = Field(default=True)
