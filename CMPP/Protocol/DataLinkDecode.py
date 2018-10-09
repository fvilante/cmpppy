from Common.Byte import Byte, Bytes, convertToBytes, fromBytesTobytes
from CMPP.Protocol.CheckSum import CheckSummerFunctor
from typing import NamedTuple, Tuple, List, Optional
from enum import Enum




Obj = bytes


# States
class State(Enum):
    INITIAL_STATE = 0
    INITIAL_ESC_RECEIVED = 1
    START_BYTE_RECEIVED = 2
    OBJECT_RECEIVING = 3
    FINAL_ESC_RECEIVED = 4
    ETX_BYTE_RECEIVED = 5
    CHECKSUM_REVEIVED = 6
    HAS_ERROR = 7
    SUCESSFUL_FRAME_RECEPTION = 8


class Tag(Enum):
    Initial_Esc = 1
    Start_Byte = 2
    Object_Data = 3
    Duplicated_Esc = 4
    Maybe_Duplicated_Esc = 5
    Final_Esc = 6
    Etx_Byte = 7
    Check_Sum = 8
    Noise = 9

    def __repr__(self):
        return f"{self.name}"


ESC = Byte(27)
ETX = Byte(3)
STX = Byte(2)
ACK = Byte(6)
NACK = Byte(21)


IsDone = bool
ParsedData = List[Tuple[Bytes, Tag]]


#functor stream analyzer
#How to use: 1) One instance per frame analyzis.
#            2) You use __call__ to insert the stream to analyze. When done return True. And then you can read 'Result' Property
#            3) If you read 'Result' before conclusion you'll get a parcial state of parsing
#            4) The result is a tuple of (byte, Tag).
class Decoder:

    def __init__(self):
        self._received: ParsedData = []  # data already processed
        self._state: State = State.INITIAL_STATE
        self._checkSummer = CheckSummerFunctor()

    # You may call this function asynchronously
    # Note: Each time this method is called it reuses the previous state. This function is statefull.
    #       When the frame analysis reaches the end the entire object become exausted, so you need to instantiate a new
    #       object to analyze next Frame.
    def __call__(self, new_bytes: bytes) -> IsDone:
        return self._analyze(convertToBytes(new_bytes))

    @property
    def result(self) -> ParsedData:
        #print(self._state)
        return self._received

    def _analyze(self, stream: Bytes) -> IsDone:
        state = self._state
        isDone: bool = False
        for byte in stream:
            #print(state, byte, self._received)
            # First ESC
            if state == State.INITIAL_STATE:
                if byte == ESC:
                    state = State.INITIAL_ESC_RECEIVED
                    self._received.append((byte, Tag.Initial_Esc))
                else:
                    self._received.append((byte, Tag.Noise))
                pass

            # Start Byte
            elif state == State.INITIAL_ESC_RECEIVED:
                if byte == STX or byte == ACK or byte == NACK:
                    state = State.START_BYTE_RECEIVED
                    state = State.OBJECT_RECEIVING
                    self._received.append((byte, Tag.Start_Byte))
                    self._checkSummer(byte.toInt())
                else:
                    state = State.INITIAL_STATE
                    self._received.append((byte, Tag.Noise))

            # Object_Data
            elif (state == State.OBJECT_RECEIVING):
                last_byte, last_tag = self._received[len(self._received)-1]
                # ESC + ESC ?
                #print(last_byte, byte)
                if (last_byte == ESC and not last_tag == Tag.Duplicated_Esc) and byte == ESC:
                    #print("Dup ESC Detected")
                    dup_esc = [(ESC, Tag.Object_Data), (ESC, Tag.Duplicated_Esc)]
                    self._received = self._received[0:len(self._received)-1] + dup_esc
                    #self._checkSummer(ESC.toInt())
                # ESC + ETX ?
                elif (last_byte == ESC and not last_tag == Tag.Duplicated_Esc) and byte == ETX:
                    #print("ESC+ETX detected")
                    esc_etx = [(ESC, Tag.Final_Esc), (ETX, Tag.Etx_Byte)]
                    self._received = self._received[0:len(self._received) - 1] + esc_etx
                    state = State.FINAL_ESC_RECEIVED
                    state = State.ETX_BYTE_RECEIVED
                    self._checkSummer(byte.toInt())
                # ESC + ANY_OTHER_THAN_ETX_OR_ESC ?
                elif last_byte == ESC and not last_tag == Tag.Duplicated_Esc:
                    #print("Received ESC + NOT(ETX or ESC) ---> So do Error!")
                    noise = [(ESC, Tag.Noise), (byte, Tag.Noise)]
                    self._received = self._received[0:len(self._received) - 1] + noise
                    state = State.HAS_ERROR
                # ANY_OTHER_THAN_ESC + ESC ?
                elif byte == ESC and (not last_byte == ESC and not last_tag == Tag.Duplicated_Esc):
                    #print("A esc to be analyzed")
                    self._received.append((ESC, Tag.Maybe_Duplicated_Esc))
                # NONE_OF_ABOVE = NORMAL DATA!
                else:
                    #print("Normal Data")
                    self._received.append((byte, Tag.Object_Data))
                    self._checkSummer(byte.toInt())

            # Checksum
            elif state == State.ETX_BYTE_RECEIVED:
                print(byte.toInt(), self._checkSummer.result)
                if byte.toInt() == self._checkSummer.result:
                    state = State.CHECKSUM_REVEIVED
                    state = State.SUCESSFUL_FRAME_RECEPTION
                    self._received.append((byte, Tag.Check_Sum))
                    isDone = True
                else:
                    self._state = State.HAS_ERROR
                    self._received.append((byte, Tag.Noise))

            # Error
            elif state == State.HAS_ERROR:
                self._received.append((byte, Tag.Noise))
                isDone = True

            elif state == State.SUCESSFUL_FRAME_RECEPTION:
                self._received.append((byte, Tag.Noise))
                IsDone = True
        pass

        self._state = state

        return isDone



def createFilter(tag: Tag):
    tag_ = tag
    def filter_(data: ParsedData) -> bool:
        #print(data)

        if data[1] == tag_:
            return True
        else:
            return False
    return filter_

# Helper to extract a Tagged byte from parsed data
def _extract(tag: Tag, data: ParsedData) -> Optional[Bytes]:
    f = createFilter(tag)
    res: Bytes = []
    for byte, _ in filter(f, data):
        res.append(byte)
    if res == []:
        return None
    else:
        return res

class FrameReceived(NamedTuple):
    parsedStream: ParsedData

    @property
    def isValid(self) -> bool:
        checksum = self.filter(Tag.Check_Sum)
        if checksum is None:
            return False
        else:
            return True

    @property
    def obj(self) -> Optional[bytes]:
        if self.isValid:
            data: Optional[bytes] = self.filter(Tag.Object_Data)
            #print(data,"*****", self.parsedStream)
            if data is None:
                return None
            else:
                return data
        else:
            return None

    @property
    def start_byte(self) -> Optional[bytes]:
        startByte: Optional[bytes] = self.filter(Tag.Start_Byte)
        if startByte is None:
            return None
        else:
            return startByte

    def filter(self, tag: Tag) -> Optional[bytes]:
        filtered: Optional[Bytes] = _extract(tag, self.parsedStream)
        if filtered is None:
            return None
        else:
            return fromBytesTobytes(filtered)

if __name__=="__main__":

    from CMPP.Protocol.DataLiinkEncode import encode

    # 1B 02 C1 50 61 02 1B 03 87
    # 1B 02 01 AC 88 89 1B 03 3D
    # 1B 02 01 B6 9C 9D 1B 03 0B
    obj_1 = [0xC1,0x50,0x61,0x02]
    obj_2 = [0x01, 0xAC, 0x88, 0x89]
    obj_3 = [0x01, 0xB6, 0x9C, 0x9D]
    obj_ = [27]
    obj = bytes(obj_3)
    stream = encode(obj, start_byte=2)
    print(stream)

    # Decode Frame
    decoder = Decoder()
    a = decoder(stream)
    # load frame with result
    frame = FrameReceived(decoder.result)

    print(frame.obj)
    print(frame.isValid)
    print(list(zip(*frame.parsedStream)))
    print(frame.start_byte)
    print(frame.filter(Tag.Check_Sum))

    pass