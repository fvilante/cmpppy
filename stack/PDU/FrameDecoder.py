from stack.PDU.FrameEncoder import timeStamp, TimeStamp
from typing import NamedTuple, Optional, List
from enum import Enum
from functools import reduce
from stack.Byte import Byte

# ---------------------
# Data Model
# ---------------------

# Core state of interpretation
class MachineState(Enum):
    WaitingOpenSignal = 1
    WaitingOpenSignal_SomeNoiseHasBeenReceived = 2
    Receiving_Object_WaitingCloseSignal = 3
    CloseSignalReceived_WaitingValidationSignal = 4
    Finished_Sucessful = 5
    Finished_ErrorHappened = 6


class State(NamedTuple):
    entered_data: Optional[bytes]
    next_byte_ref: int
    good_data: Optional[bytes]
    noise_filtered: Optional[bytes]
    currentMachineState: MachineState
    pass

def initialState():
    return State (
        entered_data = None,
        next_byte_ref = 0,
        good_data = None,
        noise_filtered= None,
        currentMachineState= MachineState.WaitingOpenSignal
    )


class Error(NamedTuple):
    pass
class Frame(NamedTuple):
    pass
class Noise(NamedTuple):
    pass

class Status(Enum):
    NotInitiated = 0
    Processing = 1
    Error = 2
    Success = 3


class Result(NamedTuple):
    status: Status
    error: Optional[Error]
    frame: Optional[Frame]
    state: State
    noise: Optional[Noise]

# ---------------------
# Functions
# ---------------------


def runMachineState(byte: Byte, state: MachineState):
    if state == M.WaitingOpenSignal:
        if
    elif state == M.WaitingOpenSignal_SomeNoiseHasBeenReceived:
    elif state == M.Receiving_Object_WaitingCloseSignal:
    elif state == M.CloseSignalReceived_WaitingValidationSignal:
    elif state == M.Finished_Sucessful:
    elif state == M.Finished_ErrorHappened:
    else:











def initializeState(initializer: Optional[State]) -> State:
    if initializer is None:
        state = initialState()
    else
        state = initializer
    return state

extractCurrentMachineStateFrom = lambda state: state.machineStateHistory[state.machineStateHistory.__len__()-1]

def interpret(byte: Byte, initializer: Optional[State]):
    state = initializeState(initializer)

    newMachineState = runMachineState(byte, state.currentMachineState)




#helper function
def decodeFrame(decoderFun:, bytes_: bytes, state: Result) -> Result:
    result = reduce(decoderFun,bytes_,state)
    return result




# ---------------------
# Test
# ---------------------

if __name__ == "__main__":

    noise = bytes([1,2,3,4,1,2])
    _1s_Result = map(decodeFrame,noise)

    newData = bytes([27,2,7,7,7,7,27])
    _2nd_Result = map(decodeFrame,newData,_1s_Result)

    lastData = bytes([3,88])
    _3rd_Result = map(decodeFrame,lastData,_2nd_Result)

    pass
