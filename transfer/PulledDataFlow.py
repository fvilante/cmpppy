from typing import Callable, List, Any, Collection
from functools import singledispatch
from typing import overload

from DataFlowBase import Size, Data

# -------------------------
# Pulled data flow model
# -------------------------
# Every output is a functin

Output = Callable[[Size], Data]

# use this function to pull data from a output
def pullData(from_: Output, size: Size) -> Data:
    data = from_(size)
    return data
# use this function if you want to convert a Collection (ie: List) into an Output to be pulled.
# note: Immutability of input collection is attended.
def collectionToOutput(collection: Collection) -> Output:
    def func(size: Size) -> Data:
        res:List[Any] = []
        for obj in collection[:size]:
            res.append(obj)
        return res
    return func



if __name__ == "__main__":

    from jUnitTest import *
    from DataFlowBase import outputFunctionBytesTest

    testCase("Connect output function to a input and sink data from input")
    k:int = 5
    probe = outputFunctionBytesTest(k)
    output = outputFunctionBytesTest
    data = pullData(output, k)
    assertIsEqual(data,probe)

    testCase("Pull data from a List[T] using some overloaded generic function")
    probe2: List[str] = ["string1","string2","string qualquer","soh um test meu"]
    data = pullData(collectionToOutput(probe2), 1000)
    assertIsEqual(data,probe2)

    testCase("Use an custom created object to dataflow.")
    class _UnknownObjectTest:
        def __init__(self,any):
            pass
    probe4: List[_UnknownObjectTest] = [_UnknownObjectTest(0),_UnknownObjectTest(1),_UnknownObjectTest(2)]
    data1 = pullData(collectionToOutput(probe4), 1000)
    assertIsEqual(data1,probe4)