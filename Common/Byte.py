from ctypes import c_uint8 as uint8_t
from typing import List

#Represents just one Byte.
class Byte:

    def __init__(self, byte: int) -> None:
        # If int is greater than 256 do a smooth reduction to byte
        while byte > 255:
            byte = byte - 256
        self._byte: int = byte  # deprecated -> uint8_t(byte).value

    def __repr__(self):
        rep: str = str(self._decimalRepresentation()) #bytes([self.value]).__repr__()
        return rep

    def __call__(self, *args, **kwargs):
        return self.value

    def __bytes__(self):
        return bytes([self._byte])

    def bit(self, bitNumber) -> bool:
        return self._byte >> bitNumber & 0x01

    def __eq__(self, other):
        return self.value == other.value

    _decimalRepresentation = lambda s: (s._byte)

    @property
    def binrep(self):
        return "0b"+bin(self.value)[2:].rjust(8, '0')

    # deprecated, use toInt insted
    @property
    def value(self) -> int:
        return self._byte

    def toInt(self) -> int:
        return self._byte

    @property
    def d0(self):
        return self.bit(0)
    @property
    def d1(self):
            return self.bit(1)
    @property
    def d2(self):
        return self.bit(2)
    @property
    def d3(self):
            return self.bit(3)
    @property
    def d4(self):
        return self.bit(4)
    @property
    def d5(self):
            return self.bit(5)
    @property
    def d6(self):
        return self.bit(6)
    @property
    def d7(self):
        return self.bit(7)



Bytes = List[Byte]

def fromBytesTobytes(b: Bytes) -> bytes:
    a = list(map(lambda x: x.toInt(), b))
    res = bytes(a)
    return res


def convertToBytes(stream: bytes) -> Bytes:
    res: List[Byte] = []
    for byte in stream:
        res.append(Byte(byte))
    return res

if __name__ == "__main__":

    # teste #1
    a = Byte(65)
    if a.value != 65 or a() !=65:
        raise KeyError()
    print("Test #1 --> Ok")

    # test #2 - converting bytes to List[Byte]
    data: bytes = bytes("00A3u41023u4123u4123u4p1234", 'utf-8')
    b: List[Byte] = convertToBytes(data)
    if b[2].value != 65:
        raise ValueError
    print("Test #2 --> Ok")

    # test #3 - operator==
    d = Byte(10)
    e = Byte(10)
    if e == e:
        print("Test #3 --> Ok")
    else:
        raise ValueError

    # test #4 - operator!=
    d = Byte(10)
    e = Byte(20)
    if d != e:
        print("Test #4 --> Ok")
    else:
        raise ValueError

    # test #4 - operator!=
    f = [Byte(65),Byte(66),Byte(67)]
    g = "abc".encode()
    h = fromBytesTobytes(f)
    if h != g:
        print("Test #5 --> Ok")
    else:
        raise ValueError



    print("Passed all Tests")

