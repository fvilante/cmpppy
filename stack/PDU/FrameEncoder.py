# Low-Level PDU (Protocol Data Unit)
# Frame construction - for transmission
from typing import NamedTuple, List, Any, Callable, Collection
from stack.Byte import Byte
from enum import Enum
from functools import partial, reduce


from stack.JuliaProtocol.Frame import Data_Object as Data, Open

from stack.JuliaProtocol.FrameInfo import *

# ------------------
# Data Model
# ------------------




class CheckSum(NamedTuple):
    check_sum: List[Byte]
    __repr__ = lambda s: str(s.bytes)

# ------------------
# Function
# ------------------

class Cmd(Enum):
    STX = Byte(2)
    ETX = Byte(3)
    ESC = Byte(27)
    ACK = Byte(6)
    NACK = Byte(21)


class Command(NamedTuple):
    MASTER_FRAME_BEGIN = Cmd.STX
    FRAME_FINISH_FOLLOWED_BY_VALIDATION = Cmd.ETX
    ESCAPE = Cmd.ESC
    SLAVE_FRAME_BEGIN = Cmd.ACK
    SLAVE_ERROR_FRAME_BEGIN = Cmd.NACK


def duplicateESC(byte_) -> bytes:
    byte = Byte(byte_)
    ESC = Command.ESCAPE
    if byte == ESC:
        return bytes([ESC,ESC])
    else:
        return byte_
    pass


# Note: obj must implement __bytes__ function
encodeData = lambda obj: Data(map(duplicateESC,bytes(obj)))
createOpen = lambda : Open(Cmd.ESC, Cmd.STX)
createClose = lambda : Close(Cmd.ESC, Cmd.ETX)

doTheSum = lambda obj: reduce(lambda x, y: x+y, bytes(obj))
twosCompliment = lambda number: 255-number
checkSumOf = lambda obj: twosCompliment(doTheSum(obj))
checksumCalculator = lambda obj: CheckSum(Byte(checkSumOf(obj)))

# Todo: TimeStamp data model class
class TimeStamp(NamedTuple):
    timeStamp: int
timeStamp = lambda : None  #Todo: time event registering


def createFrameInfo(t: Topology) -> FrameInfo:
    return FrameInfo(
        version=Version.Posijet_1,
        direction=Direction.OUTGOING,
        layerInfo='Datalink',
        topology=t,
        creationTime=timeStamp(),
        frameStrategy=[FrameElement.OPEN, FrameElement.DATA_OBJECT, FrameElement.CLOSE, FrameElement.VALIDATION]
    )





createValidator = lambda : Validator(checksumCalculator)


def frameController(t: Topology):
    open = createOpen()
    close = createClose()
    validation = createValidator()

def createFrame(t: Topology, obj) -> Frame:
    type_ = createFrameInfo(t)

    data = encodeData(obj)

    return Frame(type_, open, data, close, validation)

createFrameMaster = partial(createFrame, Topology.MASTER)
createFrameSlave = partial(createFrame, Topology.SLAVE)


# ------------------
# Tests
# ------------------


if __name__ == "__main__":

    data = [1,22,2,2]
    frame = createFrameMaster(data)
    print(frame)


    pass