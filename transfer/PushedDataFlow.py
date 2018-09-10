from typing import List, Callable, Collection
from typing import TypeVar
from DataFlowBase import Size, Data

Input = Callable[[Data], Size]

def pushData(to_: Input, data: Data) -> Size:
    return to_(data)

# -------------
# test function

def _inputFuncTest(data: Data) -> Size:
    for d in data:
        print(d)
    return len(data)

if __name__ == "__main__":


    print(pushData(to_=_inputFuncTest, data=[10,11,12,13]))