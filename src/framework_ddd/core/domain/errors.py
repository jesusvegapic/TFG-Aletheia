class DomainError(Exception):
    pass


class ApplicationError(Exception):
    pass


class EntityNotFoundError(DomainError):
    def __init__(self, entity_id: str):
        self.entity_id = entity_id


class BusinessRuleValidationError(DomainError):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
