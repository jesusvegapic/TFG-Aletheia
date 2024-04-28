class DomainError(Exception):
    pass


class EntityNotFoundError(Exception):
    def __init__(self, repository, **kwargs):
        message = f"Entity with {kwargs} not found"
        super().__init__(message)
        self.repository = repository
        self.kwargs = kwargs


class BusinessRuleValidationError(DomainError):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
