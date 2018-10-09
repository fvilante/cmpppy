# Encode obj into Posijet3 Datalink layer
from typing import Callable
from Common.Byte import Byte, Bytes, convertToBytes, fromBytesTobytes
from CMPP.Protocol.CheckSum import CheckSummerFunctor

Frame = bytes

STX: int = 2
ETX: int = 3

def encode(obj: bytes, start_byte:int=STX) -> Frame:
    fchksum = CheckSummerFunctor()
    data_ = bytes(obj)
    data = convertToBytes(data_)
    # calcula checksum
    for byte in data:
        fchksum(byte.toInt())
    fchksum(STX+ETX)
    checksum = fchksum.result

    # duplica esc
    stream: Bytes = []
    for byte in data:
        stream.append(byte)
        if byte == Byte(27):
            stream.append(Byte(27))

    # mount frame
    begin = [Byte(27),Byte(2)]
    end = [Byte(27), Byte(3), Byte(checksum)]
    frame_: Bytes = begin + stream + end
    frame: bytes = fromBytesTobytes(frame_)
    return frame




if __name__=="__main__":

    # 1B 02 C1 50 61 02 1B 03 87
    # data( 193, 80, 97, 2)
    obj = bytes([0xC1,0x50,0x61,0x02])
    obj_ = bytes([193, 80, 97, 2])
    print(encode(obj))

    print(Byte(256+255+1))



    pass