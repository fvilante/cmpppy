from typing import Callable, List, Union, TypeVar, Type
from Symbol import Symbol
from Byte import Byte
from functools import partial
from enum import Enum

# Monads types
class Data: pass
class Command: pass
class Wire: pass

# scope context
Context = TypeVar('Context', Type[Data], Type[Command], Type[Wire]) # todo: do I really need 'Type' here ?
Underlying = TypeVar('Underlying', List[Byte], List[str])

# populate sets -> create symbols

#prepare generic symbol to this context
def makeSymbol(SymbolClass: Context, numbers: Underlying) -> Symbol[Context,Underlying]:
    return Symbol(SymbolClass, numbers)

# cmpp commands (partial application)
command = partial(makeSymbol, Command)
Esc = command([Byte(27)])
Stx = command([Byte(2)])
Etx = command([Byte(3)])
Ack = command([Byte(6)])
Nack = command([Byte(21)])

# cmpp data symbols
# helper

data = lambda byte: makeSymbol(Data, [byte])





# ------------------
# Test
# ------------------

if __name__ == "__main__":

    stream : List[Symbol] = [Stx, Ack, Nack, data(9),data(30), data(30)]
    print(stream)
    print(list(map(lambda x: x.symbolClassName, stream )))