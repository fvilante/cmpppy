# Julia Protocol
# Low-Level PDU (Protocol Data Unit)
# Frame construction - for transmission
from stack.JuliaProtocol.FrameInfo import FrameInfo
from stack.JuliaProtocol.Versioning import Version
#
from typing import NamedTuple, List, Any, Callable, Collection, TypeVar, Generic, Iterable
from enum import Enum
#from functools import partial, reduce



# ------------------
# Data Model
# ------------------



class Data_Object(NamedTuple):
    data: Symbols
    def __repr__(self):
        return str(list(map(lambda x: x, self.data)))  # todo: show duplicate esc


class Frame(NamedTuple):
    type: FrameInfo
    data: List[Symbol]
    validation: Validation
    def __repr__(self):
        return f'{s.open},{s.data},{s.close},{s.validation}'



# ------------------
# Functions
# ------------------




# ------------------
# Test
# ------------------


if __name__ == "__main__":


    data = Data_Object([1])
    print(data)
    print(type(data.data))

    data = Open([2])
    print(type(data.data))
    print(data)

    data = Close([3])
    print(type(data.data))
    print(data)
