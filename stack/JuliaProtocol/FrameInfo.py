# Low-Level PDU (Protocol Data Unit)
# Frame construction - for transmission
from typing import NamedTuple, List, Any, Callable, Collection
#from stack.JuliaProtocol.Frame import FrameElement
from stack.Byte import Byte
from enum import Enum
from functools import partial, reduce


class Direction(Enum):
    OUTGOING = 1
    INCOMMING = 2

class Topology(Enum):
    MASTER = 1
    SLAVE = 2

class Version(Enum):
    Posijet_1 = 1

class AbstractDriverInfo:
    SpecificationVersion: Version

class FrameInfo(NamedTuple):
    version: Version
    layerInfo: str
    direction: Direction
    topology: Topology
    creationTime: int
    __repr__ = lambda s: f'{s.version},{s.direction},{s.topology},{s.creationTime}'



