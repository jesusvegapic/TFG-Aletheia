from abc import abstractmethod
from asyncio import Protocol


class BinaryIOProtocol(Protocol):
    @abstractmethod
    async def read(self, size: int = -1) -> bytes:
        ...
