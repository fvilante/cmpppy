
from typing import NamedTuple, List, Any, Callable, Collection, TypeVar, Generic, Iterable
from stack.JuliaProtocol.Frame import Data_Object, Symbols, Open, Close
from enum import Enum
from stack.JuliaProtocol.Versioning import Version, FakeVersion
from functools import partial



class FrameElement(Enum):
    OPEN = 1
    CLOSE = 2
    DATA_OBJECT = 3
    VALIDATION = 4


FrameStrategy = List[FrameElement]

ValidationFunction = Callable[[Data_Object], Symbols]

# Do not use this class, instead use rrameControler partial aplication
class FrameController_(NamedTuple):
    version: Version
    frameStrategy: FrameStrategy
    open: OpenCommand
    close: CloseCommand
    validator: ValidationFunction




def createFrameController(version, frameStrategy, openCommand, closeCommand, validator):
    return FrameController_(version, frameStrategy, openCommand, closeCommand, validator)