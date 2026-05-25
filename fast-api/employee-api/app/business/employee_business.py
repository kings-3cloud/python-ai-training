from datetime import date

from app.exceptions import BusinessRuleError
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeBusiness:
    """Business layer — enforces domain rules independent of persistence or HTTP."""

    @staticmethod
    def validate_create(data: EmployeeCreate) -> None:
        if data.salary <= 0:
            raise BusinessRuleError("Salary must be greater than zero")
        if data.hire_date > date.today():
            raise BusinessRuleError("Hire date cannot be in the future")

    @staticmethod
    def validate_update(data: EmployeeUpdate) -> None:
        if data.salary is not None and data.salary <= 0:
            raise BusinessRuleError("Salary must be greater than zero")
        if data.hire_date is not None and data.hire_date > date.today():
            raise BusinessRuleError("Hire date cannot be in the future")
