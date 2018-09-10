from typing import TypeVar, Collection, List, Callable # generics

# ------------
# Data Flow basic model
#
# A list of generic type T flows from inputs to outputs in a pulled or pushed way

DataObject = TypeVar('DataObject')  # generics (is the type of Object that flows)
Data = Collection[DataObject]
Size = int  # the number of data objects


# -------------
# Test Helpers
from PrimitiveTypes import Byte, Bytes, convertToBytes

def outputFunctionBytesTest(len: Size) -> List[Byte]:

    data: bytes = bytes("flaflavio test 123 12341234123412341234123412341234123412341234", 'utf-8')
    allbytes: List[Byte] = convertToBytes(data)

    res: List[Byte] = []
    for byte in allbytes[0:len]:
        res.append(byte)

    return res