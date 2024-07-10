from abc import abstractmethod
from src.framework_ddd.mailing.domain.entities import EmailMessage


class EmailSender:
    @abstractmethod
    async def send(self, email: EmailMessage):
        ...
