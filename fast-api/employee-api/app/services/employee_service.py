from app.business.employee_business import EmployeeBusiness
from app.exceptions import BusinessRuleError, EntityNotFoundError
from app.models.employee import Employee
from app.repository.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    """Service layer — orchestrates business rules and repository calls."""

    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Employee]:
        return self._repository.get_all(skip, limit)

    def get_by_id(self, employee_id: int) -> Employee:
        employee = self._repository.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundError("Employee", employee_id)
        return employee

    def create(self, data: EmployeeCreate) -> Employee:
        EmployeeBusiness.validate_create(data)
        if self._repository.get_by_email(str(data.email)):
            raise BusinessRuleError(
                f"An employee with email '{data.email}' already exists"
            )
        employee = Employee(
            first_name=data.first_name,
            last_name=data.last_name,
            email=str(data.email),
            department=data.department,
            position=data.position,
            salary=data.salary,
            hire_date=data.hire_date,
        )
        return self._repository.save(employee)

    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.get_by_id(employee_id)
        EmployeeBusiness.validate_update(data)
        if data.email is not None and str(data.email) != employee.email:
            if self._repository.get_by_email(str(data.email)):
                raise BusinessRuleError(
                    f"An employee with email '{data.email}' already exists"
                )
        update_fields = data.model_dump(exclude_unset=True)
        if "email" in update_fields:
            update_fields["email"] = str(data.email)
        for field, value in update_fields.items():
            setattr(employee, field, value)
        return self._repository.save(employee)

    def delete(self, employee_id: int) -> None:
        employee = self.get_by_id(employee_id)
        self._repository.delete(employee)
