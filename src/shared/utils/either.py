from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Union

# Definición de tipos genéricos
L = TypeVar('L')  # Tipo para Left
R = TypeVar('R')  # Tipo para Right


# Clase base abstracta para Either
class Either(ABC, Generic[L, R]):

    @abstractmethod
    def is_left(self) -> bool:
        pass

    @abstractmethod
    def is_right(self) -> bool:
        pass

    @abstractmethod
    def map(self, func: Callable[[R], R]) -> 'Either[L, R]':
        pass

    @abstractmethod
    def flat_map(self, func: Callable[[R], 'Either[L, R]']) -> 'Either[L, R]':
        pass

    @abstractmethod
    def get_or_else(self, default: R) -> R:
        pass

    @abstractmethod
    def or_else(self, default: 'Either[L, R]') -> 'Either[L, R]':
        pass


# Implementación de Left
class Left(Either[L, R]):
    def __init__(self, value: L):
        self._value = value

    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False

    def map(self, func: Callable[[R], R]) -> 'Either[L, R]':
        return self

    def flat_map(self, func: Callable[[R], 'Either[L, R]']) -> 'Either[L, R]':
        return self

    def get_or_else(self, default: R) -> R:
        return default

    def or_else(self, default: 'Either[L, R]') -> 'Either[L, R]':
        return default

    def __repr__(self):
        return f'Left({self._value})'


# Implementación de Right
class Right(Either[L, R]):
    def __init__(self, value: R):
        self._value = value

    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True

    def map(self, func: Callable[[R], R]) -> 'Either[L, R]':
        return Right(func(self._value))

    def flat_map(self, func: Callable[[R], 'Either[L, R]']) -> 'Either[L, R]':
        return func(self._value)

    def get_or_else(self, default: R) -> R:
        return self._value

    def or_else(self, default: 'Either[L, R]') -> 'Either[L, R]':
        return self

    def __repr__(self):
        return f'Right({self._value})'


# Funciones auxiliares para crear instancias de Either
def left(value: L) -> Either[L, R]:
    return Left(value)


def right(value: R) -> Either[L, R]:
    return Right(value)