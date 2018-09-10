# Haskall study
from typing import Callable, Any, List, Type, Union, Optional, TypeVar, Generic

T = TypeVar('T')

class Data(Generic[T]):
    def __init__(self, content: T, name: str) -> None:
        self._content: T = content
        self._name = name

    def __repr__(self):
        obj = f'{self._name}:{self._content}'
        return "{" + obj + "}"

    def __eq__(self, other):
        if (other._content == self._content):
            return True
        else:
            return False



class _None_:
    def __init__(self):
        self._none: bool = True

    def __repr__(self):
        return f''

    def __eq__(self, other):
        if (other._none == self._none):
            return True
        else:
            return False