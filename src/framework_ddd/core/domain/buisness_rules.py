from pydantic import BaseModel

from src.shared.domain.ddd.errors import BusinessRuleValidationError


class BusinessRule(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    __message: str = "Business rule is broken"

    def get_message(self) -> str:
        return self.__message

    def is_broken(self) -> bool:
        pass

    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"


def check_rule(rule: BusinessRule):
    if rule.is_broken():
        raise BusinessRuleValidationError(rule)


class BusinessRuleValidationMixin:
    def check_rule(self, rule: BusinessRule):
        check_rule(rule)
