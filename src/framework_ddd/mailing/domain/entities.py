from typing import List
from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.mailing.domain.value_objects import EmailSubject, EmailBody, Email


class EmailMessage(AggregateRoot):
    __to: List[Email]
    __from: Email
    __subject: EmailSubject
    __body: EmailBody

    def __init__(self, id: str, to: List[str], from_: str, subject: str, body: str):
        super().__init__(id)
        self.__to = [Email(email) for email in to]
        self.__from = Email(from_)
        self.__subject = EmailSubject(subject)
        self.__body = EmailBody(body)
