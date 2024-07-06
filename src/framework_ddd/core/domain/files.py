from abc import abstractmethod
from asyncio import Protocol


class BinaryIOProtocol(Protocol):
    @abstractmethod
    def read(self, size: int = -1) -> bytes:
        ...


class AsyncBinaryIOProtocol(Protocol):
    @abstractmethod
    async def read(self, size: int = -1) -> bytes:
        ...

    @abstractmethod
    def sync_mode(self) -> BinaryIOProtocol:
        ...
