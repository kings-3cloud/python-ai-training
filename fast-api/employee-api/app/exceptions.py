class BusinessRuleError(Exception):
    """Raised when a business rule is violated."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class EntityNotFoundError(Exception):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity: str, entity_id: int) -> None:
        self.message = f"{entity} with id {entity_id} not found"
        super().__init__(self.message)
