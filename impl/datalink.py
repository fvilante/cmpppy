#1
import abc
from typing import List, Dict, Optional, Any
#2
from cmpp.impl.memmapping import CmppParamBundle, CmppParam
from cmpp.impl.communication import CmppAvenue


# -----------------------------------------------------------------


class SerialPortInterface(abc.ABC):
    @abc.abstractmethod
    def transact(self, data: List[Any], receptionCallBack):
        '''
        An abstract interface to represent a full-duplex, non-polled
        event-driven, serial object's stream communication
        :param data: List[Any]
        :param receptionCallBack: a function that receives List[Any]
        :return: None
        '''
        pass


class ScreenPort(SerialPortStream):
    def transact(self, data: List[bytes], receptionCallBack):
        print("Transmitting...")
        print(data)
        reposta = list(bytes([1,2,3,4,5]))
        print("Receiving...")
        receptionCallBack(reposta)

# -----------------------------------------------------------------

from enum import Enum, auto
class Enum_AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

ESC = 27
STX = 2
ETX = 3
ACK = 6
NACK = 21

DIRECAO_SOLICITACAO = (0 << 6) + (0 << 7)
DIRECAO_MASCARA_RESETAR_BITS = (0 << 6) + (1 << 7)
DIRECAO_MASCARA_SETAR_BITS = (1 << 6) + (0 << 7)
DIRECAO_ENVIO = (1 << 6) + (1 << 7)

class CorePacket:
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
            int(self._dadoL),
            int(self._dadoH),
            int(ETX),
        ]
        checksum = 0
        for each in mylist:
            checksum = checksum + each
            while checksum > 256:
                checksum = checksum - 256
        checksum = 256 - checksum
        return checksum

#Packet Type enum
class PacketType(Enum_AutoName):
    PacoteDeTransmissao_Envio = auto()
    PacoteDeTransmissao_Solicitacao = auto()
    PacoteDeRetorno_DeSolicitacao_SemErro = auto()
    PacoteDeRetorno_DeEnvio_SemErro = auto()
    PacoteDeRetorno_ComErro = auto()


class PacoteDeTransmissao(CorePacket):
    def __init__(self, **xargs):
        # direcao, canal, cmd, dadoH, dadoL
        super().__init__(startByte=STX, **xargs)
    # informal interface, must implement
    @property
    def type(self):
        if self.direcao == DIRECAO_ENVIO:
            return PacketType.PacoteDeTransmissao_Envio
        elif self.direcao == DIRECAO_SOLICITACAO:
            return PacketType.PacoteDeTransmissao_Solicitacao
        else:
            return None


class PacoteDeRetorno(CorePacket):
    def __init__(self, stream: bytes):
        #todo: optimization, if stream length is to small return
        self._rawData = stream #save raw data for history analisys
        self._dictResultFromInterpreter = dict() #initialized bellow
        self._isCompleteAndValid = False
        self._hasError = False #set during this constructor if necessary
        self._corePacketType = None #this flag is set by outside class

        #interpret stream
        err_, dict_ = self._interpretStream(stream)
        self._dictResultFromInterpreter = dict_
        if err_:
            # todo: place additional diagnostic information
            self._hasError = True
            p = CorePacket(startByte=0, direcao=0, canal=0, cmd=0, dadoH=0, dadoL=0)
        else:
            #convert interpreted dict into a corePacket
            p = self._dictToCorePacket(dict_)

        #copy result to CorePacet supper-class
        super().__init__(
            startByte=p.startByte, direcao=p.direcao, canal=p.canal,
            cmd=p.cmd, dadoH=p.dadoH, dadoL=p.dadoL)
        #Well done!
        self._isCompleteAndValid = True

    # informal interface, must implement
    @property
    def type(self):
        self._corePacketType

    @property
    def rawData(self):
        return self._rawData

    @property
    def errorReport(self):
        return self._dictResultFromInterpreter

    @property
    def isCompleteAndValid(self):
        return self._isCompleteAndValid

    @property
    def hasError(self):
        return self._hasError

    class _State(Enum_AutoName):
        INITIAL_ESC = auto()  # 1
        START_BYTE = auto()  # 2
        DIRECTION = auto()  # 3.0
        CHANNEL = auto()  # 3.1
        COMMAND = auto()  # 4
        DATA_LOW = auto()  # 5
        DATA_HIGH = auto()  # 6
        FINAL_ESC = auto()  # 7
        ETX_BYTE = auto()  # 8
        CHECKSUM = auto()  # 9
        SUCESSFUL = auto()  # 10

    def _interpretStream(self, stream: bytes) -> (bool, Dict[str, Optional[int]]):
        #initialize
        pacote = list(stream)
        State = self._State
        state = State.INITIAL_ESC
        checkSum = 0
        duplicateESC = False
        dict_ = dict()

        #start analyzing stream
        for byte in pacote:

            if ((duplicateESC == True) and (byte == ESC)):
                duplicateESC = False
                continue

            #ESC-duplication code
            if ( (byte == ESC)
                    and ((state != State.INITIAL_ESC)
                         and state != (State.FINAL_ESC)) ):
                duplicateESC = True

            #Calculate checksum
            if (( (state != State.INITIAL_ESC)
                  and (state != State.FINAL_ESC))
                    and (state != State.CHECKSUM)):
                checkSum = checkSum + byte
                while checkSum > 256:
                    checkSum = checkSum - 256

            #explode bytes of packet in a dictionary
            if state == State.INITIAL_ESC:
                if (byte == ESC):
                    dict_[state] = byte
                    state = State.START_BYTE
                else:
                    dict_['ErrorDetail'] = "INITIAL_ESC failed"
                    break
                continue
            elif state == State.START_BYTE:
                #if (byte == STX) or \
                if (byte == ACK) or (byte == NACK):
                    dict_[state] = byte
                    state = State.DIRECTION
                else:
                    dict_['ErrorDetail'] = "Received startByte is not neither ACK nor NACK"
                    break
                continue
            elif state == State.DIRECTION: #or state == State.CHANNEL:
                direction = (byte >> 6) << 6
                dict_[State.DIRECTION] = direction
                state == State.DIRECTION
                dict_[State.CHANNEL] = byte - direction
                state = State.COMMAND
                continue
            elif state == State.COMMAND:
                dict_[state] = byte
                state = State.DATA_LOW
                continue
            elif state == State.DATA_LOW:
                dict_[state] = byte
                state = State.DATA_HIGH
                continue
            elif state == State.DATA_HIGH:
                dict_[state] = byte
                state = State.FINAL_ESC
                continue
            elif state == State.FINAL_ESC:
                if (byte == ESC):
                    dict_[state] = byte
                    state = State.ETX_BYTE
                else:
                    dict_['ErrorDetail'] = "FINAL_ESC failed"
                    break
                continue
            elif state == State.ETX_BYTE:
                if (byte == ETX):
                    dict_[state] = byte
                    state = State.CHECKSUM
                else:
                    dict_['ErrorDetail'] = "ETX failed"
                    break
                continue
            elif state == State.CHECKSUM:
                checkSum = 256 - checkSum  # two's complement
                dict_[state] = byte
                if (checkSum == byte):
                    state = State.SUCESSFUL
                else:
                    dict_['ErrorDetail'] = "Checksum failed"
                    break
                continue
            elif state == State.SUCESSFUL:
                dict_[state] = True
                #??
                continue
            else:
                continue

        #final step - error summary
        err_: bool = True
        if state == State.SUCESSFUL:
            dict_['Err'] = "SUCESSFUL"
            err_ = False
        else:
            dict_['Err'] = "HAS_ERROR"
            #todo: return more details of error
        return err_, dict_

    # convert result of self.interpretStream to a CorePacket class
    def _dictToCorePacket(self, dict_: Dict[str, Optional[int]]) -> CorePacket:

        State = self._State

        # todo: Assertions-> StartByte not equal to STX
        #                    CheckSum == p_.checksum

        p_ = CorePacket(
            startByte=dict_[State.START_BYTE],
            direcao=dict_[State.DIRECTION],
            canal=dict_[State.CHANNEL],
            cmd=dict_[State.COMMAND],
            dadoL=dict_[State.DATA_LOW],
            dadoH=dict_[State.DATA_HIGH]
        )

        return p_



# -----------------------------------------------------------------

from time import process_time
# Async countdown-timer
class CountDownTimer:
    def __init__(self, timeMiliseconds: int):
        self._timeToCount = timeMiliseconds

    def start(self):
        self._startTime = self._now()

    @property
    def isDone(self):
        if (self._now() - self._startTime) > self._timeToCount:
            return True
        else:
            return False

    def _now(self):  # in miliseconds
        # note: if you wanno more precision and accurary use time.perf_counter()
        return process_time()*1000


def createErrorReport(where, what: str, detail=None) -> Dict[str, Optional[str]]:
    '''
    Construct a Dict containing error information and datails
    :param where: instance of object where error occurred
    :param what: the error msg string
    :param detail:  ErrorReportable object instance that contains
                    aditional information about error contition
    :return:
    '''
    errorDetail = {
        'Descricao do erro:': what,
        'Detalhe': detail.errorReport
    }
    className = 'Classe de origem: ' + where.__class__.__name__
    errorDict_ = { className: errorDetail }
    return errorDict_



# Helper class for reception stream packet *syntactic* analyzing
# note: it must receive a copy of the sync-transmitted packege also
#       to have a better context to analyze reception
class TransactionReceptionPacketAnalyzerHelper:
    def __init__(self):
        self._receivedPacket : PacoteDeRetorno = None  # initialized by self.analyze()
        self._hasError = False
        self._hasFinishedAndIsValid = False #if after analyze it is valid
        self._errorReport = dict()

    @property
    def hasError(self):
        return self._hasError

    @property
    def errorReport(self):
        return self._errorReport

    @property
    def hasFinishedAndIsValid(self):
        return self._hasFinishedAndIsValid

    @property
    def receivedPacket(self):
        return self._receivedPacket

    # main function
    def analyze(self, data: bytes, transmittedPacket: PacoteDeTransmissao)
        # Note: PacoteDeTransmissao is given as a context to reception
        #       analyzing.
        # if an error has already occurred or if packet reception is
        # already sucessfull, don't proceed
        if self._hasError or self._hasFinishedAndIsValid:
            return
        else:
            # else, delegates packet interpretation
            pacote = PacoteDeRetorno(data)
            # save packet interpretation current state
            self._receivedPacket = pacote
            # deal with packet interpretation current state
            if not pacote.isCompleteAndValid:
                # check received data integrity
                if pacote.hasError:
                    self._reportSyntaxError()
            else:
                # packet is complete and valid
                self._hasFinishedAndIsValid = True
                self._hasError = False
                # define pacote.type property properly
                # note: accessing private property consciously
                # todo: move bellow logic do PacoteDeRetorno class
                pacote._corePacketType = self._defineReceptionPacketType(
                    transmittedPacket)
        pass #end

    def _reportSyntaxError(self) -> None:
        self._hasError = True
        errorMsg = 'Erro na sintaxe no pacote recebido'
        self._errorReport = createErrorReport(
            where=self, what=errorMsg,
            detail=self._receivedPacket)
        return

    def _defineReceptionPacketType(self, transmittedPacket: CorePacket) -> PacketType:
        if transmittedPacket.direcao == DIRECAO_ENVIO:
            type_ = PacketType.PacoteDeRetorno_DeEnvio_SemErro
        if transmittedPacket.direcao == DIRECAO_SOLICITACAO:
            type_ = PacketType.PacoteDeRetorno_DeSolicitacao_SemErro
        return type_




# note:     This is command-pattern-interface mixed with a template-pattern
#           for timer-in control. Base class also offer error-reporting facility
# note2:    'Sync' in this case means it is synched in relation to
#           remote-cmpp-server, but Async in relation  to host-cpu processing
# sub-classes:  Must implement __doTransaction, and call registerErrorReport
#               if any error occur (use also createErrorReport() helper class)
#               if communication is finished and packet is valid, sub-class must
#               _registerSuccess otherwise it must _registerErrorReport
# reponsabilities:  perform avenue transaction, count timerin, error facility for
#                   sub-classes, interface of sub-classes to client
class SyncTransactionBase(abc.ABC):

    def __init__(self, avenue: CmppAvenue):
        self._avenue = avenue
        self._countDownTimer = CountDownTimer(avenue.timerin)
        self._errorReport = dict()  # set by self._reportError()
        self._hasError = False
        self._isFinishedAndValid = False
        self._receivedPacket = None  # set by self._reportSuccess()

    @property
    def hasError(self):
        return self._hasError

    @property
    def errorReport(self):
        return self._errorReport

    @property
    def receivedPacket(self):
        return self._receivedPacket

    @property
    def isFinishedAndValid(self):
        return self._isFinishedAndValid

    def _setTimeOutError(self):
        self._hasError = True
        errorMsg = 'Erro de "time-out" no recebimento do pacote'
        self._registerErrorReport( createErrorReport(
            where=self, what=errorMsg,
            detail=self._receivedPacket))

    # -------- template method's calls -------------

    # template-method
    def doTransaction(self) -> None:
        self._doTransaction()
        # start timerin couting right after transmission
        self._countDownTimer.start()

    # template-method
    def receptionCallBack(self, data: bytes) -> None:
        # todo: who'll unregister callback?
        # if reception has finished or failed do nothing
        if self.hasError or self.isFinishedAndValid:
            return
        elif self._countDownTimer.isDone:
            # else, if timed-out setError
            self._setTimeOutError()
            return
        else:
            # else delegate to sub-class
            self._receptionCallBack(data)
            return

    # -------- template method's calls -------------

    @abc.abstractmethod
    def _doTransaction(self) -> None:
        '''
        In your sub-class you must prepare your syncPacket, when you're
        done call super()._transmit(p: PacoteDeTransmissao)
        :return: None
        '''
        pass

    @abc.abstractmethod
    def _receptionCallBack(self, data: bytes) -> None:
        '''
        In your sub-class you must implement how data bytes will be
        interpreted. Use Analyzer Helper Class has a facility
        :return: None
        '''
        pass


    # -------- facilities for templated sub-classes -------------

    #note: use createErrorReport function to generate errorReport
    def _registerErrorReport(self, errorReport: Dict[str: Optional[str]]) :
        self._hasError = True
        self._errorReport = errorReport

    def _registerSuccess(self, receivedPacket : PacoteDeRetorno):
        self._isFinishedAndValid = True
        self._receivedPacket = receivedPacket

    def _transmit(self, p: PacoteDeTransmissao):
        port = self._avenue.port
        port.transact(p.serialize(), self.receptionCallBack)


class Word_SyncTransaction(SyncTransactionBase):
    def __init__(self, param: CmppParam, avenue: CmppAvenue):
        self._param = param
        self._avenue = avenue
        self._transmittedPacket = None

    def _doTransaction(self) -> None:
        param = self._param
        # is it to send or request data?
        if param.value is None:
            # wanna *request* data to cmpp
            p = PacoteDeTransmissao_Solicitacao(
                canal=self._avenue.channel,
                cmd=self._param.key.memmap.command
            )
        else:
            # wanna *send* data to cmpp
            dadoL, dadoH = self._convertInt(self._param.value)
            p = PacoteDeTransmissao_Envio(
                canal=self._avenue.channel,
                cmd=self._param.key.memmap.command,
                dadoL=dadoL,
                dadoH=dadoH
            )
        #transmit data
        self._transmittedPacket = p  # save
        super()._transmit(p)
        pass


    def _receptionCallBack(self, data: bytes) -> None:
        # delegate reception analyzing
        analyzer = TransactionReceptionPacketAnalyzerHelper()
        analyzer.analyze(data, self._transmittedPacket )
        # process analyzer results
        if analyzer.hasFinishedAndIsValid:
            super()._registerSuccess(analyzer.receivedPacket)
        elif analyzer.hasError:
            super()._registerErrorReport( createErrorReport(
                where=self,
                what="Erro na transacao sincrona de word",
                detail=analyzer))
        else:
            return


    def _convertInt(self, value):
        if value > 255: value = 255  # todo: log error
        dado = (value).to_bytes(2, byteorder='little', signed=False)
        dadoL = dado[0]
        dadoH = dado[1]
        return dadoL, dadoH



class Bit_SyncTransaction(SyncTransactionBase):
    def __init__(self, param: CmppParam, avenue: CmppAvenue):
        self._param = param
        self._avenue = avenue

    def doTransaction(self):
        pass
    def receptionCallBack(self, data: bytes) -> None:
        pass

class Byte_SyncTransaction(SyncTransactionBase):
    def __init__(self, param: CmppParam, avenue: CmppAvenue):
        self._param = param
        self._avenue = avenue

    def doTransaction(self):
        pass
    def receptionCallBack(self, data: bytes) -> None:
        pass

class General_SyncTransaction(SyncTransactionBase):
    def __init__(self, param: CmppParam, avenue: CmppAvenue):
        self._param = param
        self._avenue = avenue

    def doTransaction(self):
        pass
    def receptionCallBack(self, data: bytes) -> None:
        pass

# select synchronous transaction strategy to adopt between host and cmpp
class TransactionerSelector(SyncTransactionBase):
    def __init__(self, param: CmppParam, avenue: CmppAvenue):
        self._strategy: SyncTransactionInterface
        #choose best strategy and initialize it
        bitlen = param.key.memmap.bitlen
        if (bitlen == 16):
            self._strategy = Word_SyncTransaction(param, avenue)
        elif (bitlen == 1):
            self._strategy = Bit_SyncTransaction(param, avenue)
        elif (bitlen == 8):
            self._strategy = Byte_SyncTransaction(param, avenue)
        else:
            self._strategy = General_SyncTransaction(param, avenue)

    def doTransaction(self):
        self._strategy.doTransaction()




# -----------------------------------------------------------------

'''
#Interface - DataLink object
#Note: All Datalink algorithm must implement this interface
class CmppDataLinkerInterface(abc.ABC):
    @abc.abstractmethod
    def transact(self, paramBundle: CmppParamBundle, avenue: CmppAvenueInterface):
        pass

    @abc.abstractmethod
    def asyncReceptionCallBack(self, data: bytes):
        pass
'''

class DataLink:

    def __init__(self, avenue: CmppAvenue):
        self._avenue = avenue
        # todo: bellow collection of attributes is common and would be extracted to a base class of all datalink module
        self._hasError = False
        self._errorReport = dict()
        self._isFinishedAndValid = False
        self._receivedPacketsList = list()  # initialized by self._transact()

    @property
    def hasError(self):
        return self._hasError

    @property
    def errorReport(self):
        # todo: may I convert this to Errable abstract class
        return self._errorReport

    @property
    def isFinishedAndValid(self):
        # todo: may I convert this to Finishable abstract class
        return self._isFinishedAndValid

    @property
    def receivedPacketsList(self):
        return self._receivedPacketsList

    def transact(self, paramBundle: CmppParamBundle):
        for param in paramBundle.list:
            self._transactSingleParam(param)

    def _transactSingleParam(self, param : CmppParam):
        # todo: rename to '...transactioner'
        transactioner_ = TransactionerSelector(param, avenue=self._avenue)
        transactioner_.doTransaction()
        if transactioner_.hasError:
            self._setOrquestrationError(detail=transactioner_)
            return
        elif transactioner_.isFinishedAndValid:
            self._isFinishedAndValid = True
            self._receivedPacketsList.append(transactioner_.receivedPacket)

    def _setOrquestrationError(self, detail):
        self._hasError = True
        errorMsg = 'Erro durante orquestracao de comunicacao'
        self._errorReport = createErrorReport(
            where=self, what=errorMsg, detail=detail)



# -----------------------------------

'''
from enum import Enum, auto
class Enum_AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class CmppProtocolType(Enum_AutoName):
    Posijet1 = auto()
    Posijet2 = auto()
    Auto_Detect = auto()


#Interface - DataLink object
#Note: All Datalink algorithm must implement this interface
class CmppAvenueInterface(abc.ABC):
    @abc.abstractmethod
    def x:
        pass

    @abc.abstractmethod
    def y:
        pass
'''



class CmppAvenue:
    def __init__(self, channel, port, timerin=800):
        if channel > 63: channel=63
        self._channel = channel
        self._port = port
        self._timerin = timerin #miliseconds
        self._datalink = DataLink()

    @property
    def channel(self):
        return self._channel

    @property
    def port(self):
        return self._port

    @property
    def protocol(self):
        return self._protocol

    @property
    def timerin(self):
        return self._timerin

    #if serial port has received data, send it to datalinker reception processor
    def update(self):
        pass

    def transact(self, paramBundle: CmppParamBundle):
        # choose appropriate data-link protocol
        from cmpp.impl.datalink import Posijet1
        if self.protocol == Posijet1:
            self._datalinker = Posijet1(avenue=self)
        else:
            raise Transmission("Cmpp Data-link protocol choosed not supported")
        # Delegate transaction
        err_, bundle_ = self.datalinker.transact(paramBundle)
        return err_, bundle_

    def transmit(self, packet : CmppPacketInterface):
        #self.state. = receiptionCallBack
        pass




if __name__ == "__main__":


    if False:
        #----------------------
        p = PacoteDeTransmissao_Envio(canal=1, cmd=60, dadoH=3, dadoL=20)
        p = PacoteDeTransmissao_Solicitacao(canal=1, cmd=60)
        resposta = [
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
        p._startByte = 0x06
        p = PacoteDeRetorno(p.serialize())
        print(p.checksum)
        p = PacoteDeRetorno(resposta)
        print(p)
        print(p.checksum)
        print(p.rawData)
        print(p._dictResultFromInterpreter)
        print(p.serialize())
        print("\n\n")
        # ----------------------

    # ----------------------
    from cmpp.impl.posReader import readPosTagTest
    paramBundle = readPosTagTest()
    avenue = FakeCmppAvenue(channel=3, port='COM1')

    datalink = Posijet1(avenue)

    err, paramBundle = datalink.transact(paramBundle, avenue)

    pass

    # ----------------------

