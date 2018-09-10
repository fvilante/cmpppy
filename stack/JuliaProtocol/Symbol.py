from typing import NamedTuple, Iterator, Callable, List, Iterable, Any, Optional, Generic, TypeVar
from enum import Enum
from functools import partial

# =============
# Data Model
# =============

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')

# Natural Numbers set
# NOTE: My design decision was to accept anything inside a container, I don't know if it is a good decision. Let it be.
Number = Any # Todo: review if Any is a good design decision. see NOTE above
Numbers = List[Number]
# Symbol spec
class Symbol(Generic[T,U]):

    def __init__(self, SymbolClass: T, numbers: U) -> None:
        self.SymbolClass: T = SymbolClass
        self.numbers: U = numbers # todo: change this name 'numbers' is not expressive

    def __repr__(self):
        return f'Symb:({self.numbers}:{self.symbolClassName})'

    def __eq__(self, other):
        c1 = (other.SymbolClass == self.SymbolClass)
        c3 = (other.numbers == self.numbers)
        if (c1 and c3):
            return True
        else:
            return False

    @property
    def symbolClassName(self) -> str:
        # extract class name
        s: str = str(self.SymbolClass)
        a: List = s.split('.')
        txt = str(a[len(a) - 1])
        res = txt[:len(txt) - 2]
        return res

Symbols = List[Symbol]


#Symbol Channel is buffered, push/pull-input pull-output port.
Size = int
ChannelName = str
class SymbolChannel: # todo: make this class generic

    def __init__(self, channelName: ChannelName = None, initializer: Symbols = []) -> None:
        self._channelName = channelName
        self._buffer: Symbols = initializer

    def put(self, symbols: Symbols) -> Size:
        self._buffer = self._buffer + symbols
        return len(symbols) # in PC we can afford load all bytes (supose infinite memory)

    def take(self, size: Size) -> Symbols:
        taked : Symbols = self._buffer[:size]
        remaining: Symbols = self._buffer[size:]
        self._buffer = remaining
        return taked

    def __repr__(self):
        return f'buf_{self._channelName}:{self._buffer}'


# =============
# Functions
# =============

# private

__createSymbolChannel = lambda *args: SymbolChannel(*args)
__identityFunction = lambda x: x


# Public

def createSymbol(SymbolClass: T, numbers: K) -> Symbol[T,K]:
    return Symbol(SymbolClass, numbers)


# =============
# Tests
# =============


class Data: pass
class Command: pass


# Test Symbol{T] semantics:
#def func(data: Symbol[Data]) -> Symbol[Command]:
#    f = lambda x: x
#    commandSet = createSymbolSet(Data, f)
#    cmd = createSymbol(commandSet, [65], '65')
#    return cmd



if __name__ == "__main__":


    # Symbol creation
    # Checking if generic type, and type checking is working right
    a = createSymbol(Data, [65])
    b = Symbol(Data,[65])
    a.numbers = [62, 65]
    b.numbers = [62, 65]
    #reveal_type(a)
    #reveal_type(b)

    data_A = createSymbol(Data, [65])
    data_A_YES = createSymbol(Data, [65])
    data_A_NO = createSymbol(Command, [65])
    print('&&&&&&')
    assert(data_A == data_A_YES)
    assert(data_A != data_A_NO)
    command_Nack = createSymbol(Command, [27, 21])
    print(data_A)


    # Todo: It's not safe. The Symbol[T] semantics doesn't works. Don't know what to do now, I'll proced as is and try solve it later
    # Test Symbol{T] semantics:
    print('-----')
    print(type(command_Nack))
    print(type(data_A))
    #z = func(data_A)
    print('-----')


    # Symbol Channel creation
    chan = __createSymbolChannel("test")
    print(chan)
    print(chan.put([data_A, command_Nack, data_A]))
    print(chan)
    print(chan.take(1))
    print(chan)


    print(type(data_A.numbers))

    print(data_A.symbolClassName)

    print(data_A.numbers)



    pass