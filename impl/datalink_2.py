import abc
from typing import Dict, List, Optional, Any

# ------------------------------------------------------
from enum import Enum, auto
class Enum_AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class ErrorReport:
    def __init__(self, who, what: str, detail: Optional[Dict[Any,Any]]=None):
        '''
        :param who: instance of object where error occurred
        :param what: the error msg string
        :param detail:  ErrorReportable object instance that contains
                        aditional information about error contition
        '''
        self._who = who
        self._what = what
        self._detail = detail

    @property
    def dict(self):
        return self._createErrorReportDict()

    def __str__(self):
        return self.dict

    #facility function
    def _createErrorReportDict(self) -> Optional[Dict[Any,Any]]:
        '''
        Construct a Dict containing error information and datails
        '''
        who = self._who
        what = self._what
        detail = self._detail
        errorDetail = {
            'Descricao do erro:': what,
            'Detalhe': detail
        }
        className = 'Classe de origem: ' + who.__class__.__name__
        errorDict_ = { className: errorDetail }
        return errorDict_


# ------------------------------------------------------

class _Errable_Abstract_(abc.ABC):

    @property
    @abc.abstractmethod
    def errorReport(self) -> ErrorReport:
        '''
        :return:    (ErrorReport instance: it encapsulates a dict containing
                    error information.)
        '''
        pass

    @property
    @abc.abstractmethod
    def hasError(self) -> bool:
        '''
        Only true if registerErrorReport has been called once
        :return:
        '''
        pass

    @abc.abstractmethod
    def registerError(self, e: ErrorReport):
        '''
        Automatic sets hasError proterty and stores e object
        '''
        pass

class Errable(_Errable_Abstract_):

    def __init__(self):
        self._hasError = False
        self._errorReport = None

    def errorReport(self) -> Optional[Dict[Any,Any]]:
        return self._errorReport

    def hasError(self) -> bool:
        return self._hasError

    def registerError(self, e: ErrorReport):
        self._errorReport = e


class _Finishable_Abstract_(abc.ABC):
    '''
    If someshing may finish, it is finishable
    '''
    @property
    @abc.abstractmethod
    def hasFinished(self) -> bool:
        '''
        Call it to check if something has finished.
        :return:    true if registerFinish has not been called,
                    false otherwise
        '''
        pass

    @abc.abstractmethod
    def registerFinish(self) -> None:
        '''
        call it when you reach the finish of something
        :return: None
        '''
        pass

class Finishable(_Finishable_Abstract_):

    def __init__(self):
        self._hasFinished = False

    @property
    def hasFinished(self):
        return self._hasFinished

    def registerFinish(self):
        self._hasFinished = True

class CarrierProtocol(Errable, Finishable):
    pass

# Note: Serialization is to put any kind of object in serie.
class Serializable(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> List[Any]:
        pass

# -------------


class BinaryEncodable(abc.ABC):
    @abc.abstractmethod
    def encode(self) -> Optional[bytes]:
        pass


class BinaryDecoder(abc.ABC):
    @abc.abstractmethod
    def decode(self, data: bytes) -> None:
        pass

# -------------
# DataObject for Posijet1 protocol
class CorePacket(Serializable):
    def __init__(self, *, startByte, direcao, canal, cmd, dadoH, dadoL):
        self._startByte = startByte
        self._direcao = direcao
        self._canal = canal
        self._direcao_e_canal = int(direcao + canal)
        self._cmd = cmd
        self._dadoH = dadoH
        self._dadoL = dadoL

    @property
    def startByte(self):
        return self._startByte

    @property
    def direcao(self):
        return self._direcao

    @property
    def canal(self):
        return self._canal

    @property
    def direcao_e_canal(self):
        return self._direcao_e_canal

    @property
    def cmd(self):
        return self._cmd

    @property
    def dadoH(self):
        return self._dadoH

    @property
    def dadoL(self):
        return self._dadoL

    @property
    def checksum(self):
        return self._calculateChecksum()

    def serialize(self):
        return self._toBytes()

    def _duplicateIfEsc(self, value: int) -> List[int]:
        r_ = [value]
        if value == ESC:
            r_.append(ESC)
        return r_

    def _toBytes(self) -> bytes:

        pacote = [
            [ESC, self.startByte],
            self._duplicateIfEsc(self._direcao_e_canal),
            self._duplicateIfEsc(self._cmd),
            self._duplicateIfEsc(self._dadoL),
            self._duplicateIfEsc(self._dadoH),
            [ESC, ETX],
            self._duplicateIfEsc(self.checksum)
        ]

        #pacote = [[1],[2],[3],[3],[6],[7]]
        list_of_bytes = [item for sublist in pacote for item in sublist]
        return bytes(list_of_bytes)

    def _calculateChecksum(self) -> int:
        mylist = [
            int(self.startByte),
            int(self.direcao),
            int(self.canal),
            int(self.cmd),
            int(self.dadoL),
            int(self.dadoH),
            int(ETX),
        ]
        checksum = 0
        for each in mylist:
            checksum = checksum + each
            while checksum > 256:
                checksum = checksum - 256
        checksum = 256 - checksum
        return checksum



# functor - encapsulates chacksum logic
class CheckSummerFunctor:
    def __init__(self):
        self._checksum=0  # without two's compliment

    @property
    def result(self) -> int:
        # two's compliment it and the fly
        checksum_ = 256 - self._checksum
        return checksum_ #two's complimented

    # Attention: singleByte type is int
    def __call__(self, singleByte: int) -> None:
        if not isinstance(singleByte, int):
            raise TypeError("ChecksumFunctor chamado com tipo de valor invalido")
        else:
            self._checksum += singleByte
            while self._checksum > 256:
                self._checksum -= 256



# objects to abstract data, Von Neuman concepts: everything is data,
# including code.

class Checksummable(abc.ABC):
    @abc.abstractmethod
    def checksum(self) -> int:
        pass

# ------------------

ESC = 27
STX = 2
ETX = 3
ACK = 6
NACK = 21

class BaseCode(Checksummable, BinaryEncodable):
    pass

class Command(BaseCode):
    def __init__(self, cmd: int):
        # todo: validation log warning
        if cmd >255: cmd = 255
        if cmd < 0:  cmd = 0

        self._cmd = cmd

    def encode(self) -> bytes:
        # todo: extract esc from here
        return bytes([ESC, self._cmd])

    def checksum(self) -> int:
        return self._cmd


class Data(BaseCode):
    def __init__(self, dataObject: BinaryEncodable):
        self._rawDataObject = dataObject  # const 'original' data

    def encode(self) -> bytes:
        return self._encodeWithDuplicateESC()

    def _encodeWithDuplicateESC(self) -> bytes:
        encoded_: bytes = b''
        for byte in self._encode():
            if byte == ESC:
                encoded_ += bytes([byte]) + bytes([ESC])
            else:
                encoded_ += bytes([byte])
        return encoded_

    def _encode(self) -> bytes:
        # check if data object is a BinaryEncodabele interface implementation
        if hasattr(self._rawDataObject,'encode'):
            encoded_:bytes = self._rawDataObject.encode()
        else:
            #try python standard-method (good for standard objects encoding)
            encoded_:bytes = bytes(self._rawDataObject)
        return encoded_

    def checksum(self) -> int:
        # algorithm: sum all bytes, if is a duplicate ESC, just sum one ESC
        ESC = 27
        lastByte = None
        checksum_calculator_ = CheckSummerFunctor()
        for byte in list(self.encode()):
            if byte == ESC and lastByte == ESC:
                lastByte = None
                continue
            else:
                lastByte = byte
                checksum_calculator_(byte)
        return checksum_calculator_.result


# --------------

#helper
def _checkIfTypeIsByte(data: bytes) -> bytes:
    # try some type coercion before give up
    if isinstance(data, bytes):
        result_ = data
    elif isinstance(data, list):
        result_ = bytes(data)
    else:
        #todo: eventually try to convert or log a warnning and continue
        raise TypeError()
    return result_




class CheckSum(BaseCode):
    def __init__(self, baseObjects: List[BaseCode]):
        self._baseObjects = baseObjects
        self._checkSumCalculator = CheckSummerFunctor()
        #calculate checksum
        for each in self._baseObjects:
            byte = each.checksum()
            self._checkSumCalculator(12)

    def encode(self) -> bytes:
        return bytes([self._checkSumCalculator.result])

    def checksum(self) -> int:
        return self._convertToInt(self.encode())

    def _convertToInt(self, n: int) -> int:
        return list(n)[0]

# Carrier stands for the layer level
class CmppEncoder(BinaryEncodable):

    def __init__(self, dataObject: Serializable):
        self._data = dataObject

    def encode(self) -> bytes:
        codeBlocks = self._makeCodeBlocks()
        return self._encode(codeBlocks)

    def _makeCodeBlocks(self) -> List[BaseCode]:
        START_TRANSMISSION = STX = 2
        END_TRANSMISSION = ETX = 3
        stx = Command(START_TRANSMISSION)
        etx = Command(END_TRANSMISSION)
        codeBlocks_: List[BaseCode] = [stx, self._data, etx]
        codeBlocks_.append(CheckSum(codeBlocks_))
        return codeBlocks_

    def _encode(self, codeBlocks: List[BaseCode]) -> bytes:
        encoded_:bytes = b''
        for each in codeBlocks:
            encoded_ += each.encode()
        return encoded_

# -----------------------------


class InputStreamPipe(abc.ABC):
    @abc.abstractmethod
    def input(self, input: Optional[List[BinaryEncodable]]) -> None:
        pass

class OutputStreamPipe(abc.ABC):
    @abc.abstractmethod
    def output(self) -> Optional[List[BinaryEncodable]]:
        pass

class StreamPipe(InputStreamPipe, OutputStreamPipe):
    pass

class StreamBufferStage(StreamPipe):
    def __init__(self, len: int=0):
        self._binaryQueue = bytes()
        self._stageQueue = bytes()
        self._len = len

    def input(self, input: List[BinaryEncodable]) -> None:
        if input is None:
            return
        for each in input:
            self._binaryQueue += each.encode()

    def output(self) -> Optional[List[BinaryEncodable]]:
        lendiff:int = len(self._binaryQueue) - self._len
        if lendiff > 0:
            # open gate, move data
            # fifo. First-out is considered the list[0] element
            obj = Data(self._binaryQueue[0:lendiff])
            self._binaryQueue = self._binaryQueue[lendiff+1:]
            return [obj] #returns a list
        else:
            # close gate block dataflow
            return None

# ------------------

class _Gate_Abstract_(abc.ABC):

    @property
    @abc.abstractmethod
    def isOpened(self):
        pass

    @abc.abstractmethod
    def registryOpenned(self):
        pass

    @abc.abstractmethod
    def registryClosed(self):
        pass

class Gatable(_Gate_Abstract_):
    def __init__(self, isOpened: bool):
        self._isOpened = isOpened

    @property
    def isOpened(self):
        return self._isOpened

    def registryOpenned(self):
        self._isOpened = True

    def registryClosed(self):
        self._isOpened = False

class NormalyClosedGate(StreamPipe, Gatable):
    def __init__(self, compare: BinaryEncodable):
        Gatable.__init__(self)
        self._compare = compare
        self._gate_helper = StreamBufferStage(len=0) # code reuse

    def input(self, input: Optional[List[BinaryEncodable]]) -> None:
        # delegates, always sink, and gate logic controls only the sourcing...
        self._gate_helper.input(input=input)

    def output(self) -> Optional[List[BinaryEncodable]]:
        if Gatable.isOpened:
            return self._gate_helper.output()
        else:
            return None

class NormalyOpenGate(StreamPipe, Gatable):
    pass

# ---------

class StreamDriver(StreamPipe):

    def input(self, input: Optional[List[BinaryEncodable]]) -> None:
        filter = Filter(OrGate(Command(ACK), Command(NACK))):

    def check_for_Nack(self):
        checker = Checker(Command(Ack))
        output1 = Noise()
        output2 = Data_Block()
        swicth_nack = Swith(input, output1, output2, checker)

    def check_for_Ack(self):
        checker = Checker(Command(Ack))
        output1 = switch_nack
        output2 = Data_Block()
        swicth1_ack = Swith(input, output1, output2, checker)





class SingleDecoderComparator(BinaryDecoder, Finishable):
    '''
    Compares stream of bytes with a list of BinaryEncodable objects.
    if any part of the stream matchs, Finishable interface is set
    '''
    def __init__(self, filterObject: BinaryEncodable):
        Finishable.__init__(self)
        self._filterObject = filterObject
        self._binaryFilter = filterObject.encode()
        self._rawData:bytes = bytes() #original input data

    def decode(self, stream: bytes) -> None:
        for byte in stream:
            self._processOneByte(bytes([byte]))

    def _processOneByte(self, byte: bytes) -> None:
        self._rawData += byte
        print(self._rawData, self._binaryFilter)
        #compare stream
        if self._rawData == self._binaryFilter:
            #if Match!
            Finishable.registerFinish(self)
        else:
            pass


class DecoderComparator(BinaryDecoder, Finishable):
    def __init__(self, list_: List[BinaryEncodable]):
        Finishable.__init__(self)
        self._list = []
        for each in list_:
            #wrap each BinaryEncodable in a SingleDecoderComparator
            self._list.append(SingleDecoderComparator(each))

    def decode(self, stream: bytes) -> None:
        for singleComparator in self._list:
            a = singleComparator
            a.decode(stream)
            if a.hasFinished:
                Finishable.registerFinish()

class CmppDecoder2(BinaryDecoder, Finishable, Errable):

    def __init__(self):
        Finishable.__init__()
        Errable.__init__()
        #internal state
        self._state = self._State.NOISE
        self._rawBytesData = bytes()

    class _State(Enum_AutoName):
        NOISE = auto()
        START_FRAME = auto()
        DATA_OBJECT = auto()
        END_FRAME = auto()
        CHECKSUM = auto()
        HAS_ERROR = auto()
        SUCESSFUL = auto()

    def decoder(self, stream: bytes) -> None:
        stream = _checkIfTypeIsByte(stream)
        State = self._State

        if self._state == State.NOISE:
            #wait for ack or nack
            comp_ack = BinaryDecoderComparator(Command(ACK))
            comp_nack = BinaryDecoderComparator(Command(NACK))
            comp_ack.decode(stream)
            comp_nack.decode(stream)
            if comp_ack.hasFinished or comp_nack.hasFinished:
                self._state = State.START_FRAME
            else:
                pass
        if self._state == State.START_FRAME:
            pass




'''
class CmppDecoder(BinaryDecoder, Finishable, Errable):

    class _State(Enum_AutoName):
        NOISE = auto()
        START_BLOCK = auto()
        DATA_OBJECT = auto()
        END_BLOCK = auto()
        CHECK_SUM = auto()
        HAS_ERROR = auto()
        SUCCESSFUL = auto()

    def __init__(self):
        # initial state
        self._state = self._State.NOISE  #before a start_block everything is considered noise
        self._codeStream: List[BaseCode] = [] # list of decoded objects
        self._rawDataObject: bytes = b'' #data must be stored between async calls to decode
        self._noiseData: bytes = b'' # any information not recognized is considered noise
        self._lastByteHasBeenDoubleEsc: bool = False
        self._rawData: bytes = b''




    def decode(self, data: bytes) -> None:
        data = _checkIfTypeIsByte(data)  # if possible converts it

        self._rawData += data #  store raw material

        # super class init
        Finishable.__init__(self)
        Errable.__init__(self)

        # state
        State = self._State  # const
        state = self._state  # variable
        noise_data = self._noiseData
        codeStream = self._codeStream
        print(self._rawData)

        codeStream: List[BaseCode]
        print('oi')
        # Note: a = current byte, b = peek on next byte of the stream
        for a, b in zip(data,data[1:]):
            print(self._rawData)
            print(a,b, state)
            # Remember: Noise is our initial state
            if state == State.NOISE:
                # only noise state can open the block everything-else is considered noise
                if [a, b] == [ESC, ACK] or [a,b] == [ESC, NACK]:
                    state = State.START_BLOCK
                    start_block = Command(b)
                    codeStream.append(start_block)
                    continue
                else:
                    noise_data += a
                    continue
            elif state == State.START_BLOCK:
                # a kind of 'nop' operation to step forward interation
                state = State.DATA_OBJECT
                continue
            elif state == State.DATA_OBJECT:

                # second double esc? escape
                if self._lastByteHasBeenDoubleEsc == True:
                    self._lastByteHasBeenDoubleEsc = False
                    continue
                else:
                    #else if end block detected
                    if [a,b] == [ESC, ETX]:
                        print("oi7******")
                        state = State.END_BLOCK
                        continue
                    #else if doble ESC detected
                    elif [a, b] == [ESC, ESC]:
                        data += a
                        self._lastByteHasBeenDoubleEsc = True
                        continue
                    # normal data
                    else:
                        print("oi5******")
                        self._rawDataObject += bytes([a])   #collect information
                        continue

            elif state == State.END_BLOCK:
                codeStream.append(Data(self._rawDataObject)) #wrap decoded data
                end_block = Command(ETX)
                codeStream.append(end_block)
                state = State.CHECK_SUM

                #Checksum verification code bellow
                print('oi3')
                checksum_block = CheckSum(codeStream)
                print(hex(checksum_block.checksum()))
                print('oi3')
                if checksum_block.checksum() == a:
                    codeStream += checksum_block
                    state = State.SUCCESSFUL
                    Finishable.registerFinish()  # success!
                else:
                    Errable.registerError(self=self, e=ErrorReport(who=self, what='Checksum invaido',detail=None))
                    #raise RuntimeError("Checksum invalid")
                break

        self._state = state  # variable
        self._noiseData = noise_data
        self._codeStream = codeStream

'''

if __name__ == "__main__":

    data = Data([5,10,15,20])
    test = Data([5,10,15,21])
    stage = StreamBufferStage(2)
    stage.input([data])
    print("input")
    print(list(data.encode()))
    print("dentro")
    print(stage._)
    print("output")
    print(list(stage.output()[0].encode()))


    #comp = BinaryDecoderComparator(data)
    #comp.decode(test.encode())
    #print(comp.hasFinished)
    # BinaryDecoderComparator


'''
    a = bytes([1,2,3,4,5])
    data = Data(a)

    load = CmppEncoder(data)

    stream:bytes = CorePacket(
        startByte=6,
        direcao=0,
        canal=1,
        cmd=60,
        dadoL=3,
        dadoH=4
    ).serialize()

    stream = [
        ESC,
        ACK,
        0xC1,
        0x52,
        0x00,
        0x00,
        ESC,
        ETX,
        0xE4,
    ]

    stream = bytes(stream)
    print(stream.hex())
    decoder = CmppDecoder()
    decoder.decode(stream)
    print(decoder.hasError())
    print(decoder.hasFinished)
    print(decoder._rawData)
    print(decoder._state)
    print(decoder._codeStream[0].encode())
    print(decoder._codeStream[1].encode())
    print(decoder._codeStream[2].encode())
    print(decoder._rawDataObject)

'''


