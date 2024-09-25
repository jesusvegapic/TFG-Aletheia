from dataclasses import dataclass


class DomainError(Exception):
    pass


class ApplicationError(Exception):
    pass

@dataclass(frozen=True)
class EntityNotFoundError(DomainError):
    entity_id: str


class BusinessRuleValidationError(DomainError):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
