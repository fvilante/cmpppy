from typing import Callable, Any, List, Iterator
from Byte import Byte, Bytes, convertToBytes
from Symbol import Symbol, Symbols, createSymbol
from Commands import Esc, Stx, Ack, Nack, Etx, Command, Data, Wire, command, data
from functools import partial, reduce

WireSymbolFlow = List[Symbol[Wire, List[Byte]]]

#flat list
flatten = lambda l: [item for sublist in l for item in sublist]
flatMap = lambda f,x: list(map(f,x))


def checksum(obj: bytes) -> Bytes:
    sum = reduce(lambda x,y: x+y, obj)
    res = value = Byte(sum)
    res = twosCompliment = Byte(255-value.toInt())
    return [res]

def dup_esc(b: Byte) -> Bytes:
    res: Bytes = [b]
    if b == Byte(27):
        res.append(Byte(27))
    return res

Data = Symbol[Data,Bytes]

def objToByte(obj: bytes) -> List[Data]:
    return flatMap(lambda x: Byte(x), obj)

class Frame: pass


def theProcess(obj: bytes):
    # convert obj to bytes
    # calc_validation
    # define stream
    validation = checksum(obj)
    open_ = ([Esc, Stx],"Open","Open_Master",["Esc", "Stx"])
    close_ = ([Esc, Etx, validation],"Close", "Close_WithValidation", ["Esc", "Etx", "CheckSum"])
    data_ = ([objToByte(obj)], "Data","Data_Object",f)
    frame = (open_, data_, close_)
    return flatten(frame)



if __name__ == "__main__":

    obj = bytes([1,20,10,27,28,29])

    data = checksum(obj)
    data = objToByte(obj)
    data = theProcess(obj)
    print(data)
    #print(list(map(lambda x: symbolClassName(x), data)))

    pass