from sqlmodel import Session, select

from app.models.employee import Employee


class EmployeeRepository:
    """Repository layer — all database access for Employee lives here."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Employee]:
        return list(
            self._session.exec(select(Employee).offset(skip).limit(limit)).all()
        )

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self._session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return self._session.exec(
            select(Employee).where(Employee.email == email)
        ).first()

    def save(self, employee: Employee) -> Employee:
        self._session.add(employee)
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self._session.delete(employee)
        self._session.commit()
