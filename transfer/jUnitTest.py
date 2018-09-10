from typing import TypeVar

# ------------
# Test library

_TestType = TypeVar('_TestType') # generics (T is the type of Object that flows)


testNumber: int = 0

def testCase(name:str):
    global testNumber
    testNumber += 1
    if testNumber == 1: print("\nRUNNING UNIT TESTS:\n")
    msg: str = f"\tTest #{testNumber} - {name} --> "
    print(msg, end='')
    return

def assertIsEqual(data:_TestType,probe:_TestType) -> bool:
    if data != probe:
        print("\nASSERTION ERROR: (==)")
        print(f"\tData:\t{type(data)}\t{data}")
        print(f"\tProbe:\t{type(data)}\t{probe}")
        print(flush=True)
        raise ValueError()
    else:
        print("| PASSED |")
        return True