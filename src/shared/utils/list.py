from itertools import chain
from typing import TypeVar, Callable, List, Optional, Iterable

X = TypeVar('X')
T = TypeVar('T')


def flatmap(f: Callable[[X], T], xs: Iterable[X]):
    return chain.from_iterable(map(lambda elem: f(elem), xs))  # type: ignore


def find(exp: Callable[[T], bool], listToSearch: Iterable[T]) -> Optional[T]:
    for elem in listToSearch:
        if exp(elem):
            return elem
    return None
